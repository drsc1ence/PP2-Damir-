import psycopg

def connect_and_test(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            upsert_term_first = input("Please, enter first name input: ")
            upsert_term_last = input("Please, enter last name input: ")
            upsert_term_phone = input("Please, enter phone number input: ")
            conn.execute("CALL upsert_contact(%s, %s, %s)", (upsert_term_first, upsert_term_last, upsert_term_phone))
            conn.commit()
            
            
            return conn
    except (psycopg.DatabaseError, Exception) as error:
        print(error)

def load_config():
    config = {
        'host': 'localhost',
        'dbname': 'newphonebook',  # <--- Change this line right here!
        'user': 'postgres',
        'password': 'damir2007'
    }
    return config
if __name__ == '__main__':
    config = load_config()
    connect_and_test(config)