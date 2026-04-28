import psycopg
from jsonto import export_to_json


def connect_and_test(config):
    """Connect to the PostgreSQL database server with pagination loop"""
    try:
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            export_to_json(conn)
    except (psycopg.DatabaseError, Exception) as error:
        print(error)


def load_config():
    return {
        'host': 'localhost',
        'dbname': 'newphonebook',
        'user': 'postgres',
        'password': 'damir2007'
    }


if __name__ == '__main__':
    config = load_config()
    connect_and_test(config)