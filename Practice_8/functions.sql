CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT r.first_name, r.last_name, r.phone_number FROM residence r
                 WHERE r.first_name ILIKE '%' || p || '%'
                 OR r.last_name ILIKE '%' || p || '%'
                    OR r.phone_number ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;