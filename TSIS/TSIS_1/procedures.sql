CREATE OR REPLACE FUNCTION filter_by_group(group_name VARCHAR)
RETURNS TABLE (first_name VARCHAR, last_name VARCHAR, email VARCHAR, birthday DATE)
LANGUAGE plpgsql AS $$
BEGIN 
RETURN QUERY 
SELECT r.first_name, r.last_name, r.email, r.birthday FROM residence r JOIN groups g ON r.group_id = g.id WHERE g.name = group_name;
END; $$;


CREATE OR REPLACE FUNCTION get_email_by_pattern(e text)
RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, email VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT r.first_name, r.last_name, r.email, p.phone FROM residence r LEFT JOIN phones p ON r.residence_id = p.residence_id
                 WHERE r.email ILIKE '%' || e || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION sort_contacts(sort_criteria VARCHAR)
RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, email VARCHAR, birthday DATE) AS $$
BEGIN 
    RETURN QUERY EXECUTE format('SELECT first_name, last_name, email, birthday FROM residence ORDER BY %I ASC', sort_criteria);
END;
$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS get_paginated(integer, integer);

CREATE OR REPLACE FUNCTION get_paginated(lim INT, off INT)
RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, email VARCHAR, birthday DATE)
AS $$
BEGIN
    RETURN QUERY
    SELECT r.first_name, r.last_name, r.email, r.birthday
    FROM residence r
    ORDER BY r.residence_id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    rid INT;
BEGIN
    -- ищем контакт (предполагаем first_name)
    SELECT residence_id INTO rid
    FROM residence
    WHERE first_name = p_contact_name;

    IF rid IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones(residence_id, phone, type)
    VALUES (rid, p_phone, p_type);

END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    rid INT;
    gid INT;
BEGIN
    -- найти контакт
    SELECT residence_id INTO rid
    FROM residence
    WHERE first_name = p_contact_name;

    IF rid IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    -- найти группу
    SELECT id INTO gid
    FROM groups
    WHERE name = p_group_name;

    -- если нет группы → создать
    IF gid IS NULL THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO gid;
    END IF;

    -- обновить контакт
    UPDATE residence
    SET group_id = gid
    WHERE residence_id = rid;

END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT r.first_name, r.last_name, r.email, p.phone
    FROM residence r
    LEFT JOIN phones p ON r.residence_id = p.residence_id
    WHERE 
        r.first_name ILIKE '%' || p_query || '%'
        OR r.last_name ILIKE '%' || p_query || '%'
        OR r.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%';
END;
$$;