import psycopg

def connect_and_test(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            limit = int(input("Enter limit of pagination: "))
            offset = int(input("Enter offset of pagination: "))
            
            sql = "SELECT * FROM get_paginated(%s, %s);"
            search_result = conn.execute(sql, (limit, offset))
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