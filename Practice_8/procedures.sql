CREATE OR REPLACE PROCEDURE upsert_contact(f_name VARCHAR, l_name VARCHAR, p_number VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM residence WHERE first_name = f_name AND last_name = l_name) THEN
        UPDATE residence SET phone_number = p_number WHERE first_name = f_name AND last_name = l_name;
    ELSE
        INSERT INTO residence(first_name, last_name, phone_number) VALUES(f_name, l_name, p_number);
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION upsert_many(f_names VARCHAR[], l_names VARCHAR[], p_numbers VARCHAR[])
RETURNS SETOF residence
LANGUAGE plpgsql AS $$
DECLARE i INT; bad_record residence;
BEGIN
    FOR i IN 1 .. array_length(f_names, 1) LOOP
        IF p_numbers[i] SIMILAR TO '87[0-9]{9}' THEN
            IF EXISTS (SELECT 1 FROM residence WHERE first_name = f_names[i] AND last_name = l_names[i]) THEN
                UPDATE residence SET phone_number = p_numbers[i] WHERE first_name = f_names[i] AND last_name = l_names[i];
            ELSE
                INSERT INTO residence(first_name, last_name, phone_number) VALUES(f_names[i], l_names[i], p_numbers[i]);
            END IF;
        ELSE
            bad_record.first_name := f_names[i];
            bad_record.last_name := l_names[i];
            bad_record.phone_number := p_numbers[i];
            
            -- 3. Return the properly formatted record
            RETURN NEXT bad_record;
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by_name(f_name VARCHAR, l_name VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM residence
    WHERE first_name = f_name AND last_name = l_name;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by_number(p_number VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM residence
    WHERE phone_number = p_number;
END;
$$;