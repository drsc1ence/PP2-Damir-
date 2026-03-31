import psycopg

def connect_and_test(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            f_name = input("Enter first name to delete: ")
            l_name = input("Enter last name to delete: ")
            
            sql = "CALL delete_contact_by_name(%s, %s);"
            conn.execute(sql, (f_name, l_name))
            search_result = conn.execute("SELECT * FROM residence;")
            search_rows = search_result.fetchall()
            for row in search_rows:
                print(row)
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