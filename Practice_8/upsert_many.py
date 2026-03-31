import psycopg

def connect_and_test(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            sql = "SELECT * FROM upsert_many(ARRAY['Ernar', 'Kairat'], ARRAY['Nurtas', 'Arsenov'], ARRAY['87472305060', '877650430']);"
            search_result = conn.execute(sql)
            search_rows = search_result.fetchall()
            for row in search_rows:
                print("INCORRECT FORMAT OF PHONE NUMBER")
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