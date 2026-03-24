import psycopg
from config import load_config

def get_residences():
    """ Retrieve data from the residences table """
    config  = load_config()
    try:
        with psycopg.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT residence_id, first_name, last_name FROM residence ORDER BY first_name;")
                print("The number of residences: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()

    except (Exception, psycopg.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    get_residences()