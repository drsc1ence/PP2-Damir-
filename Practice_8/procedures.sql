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