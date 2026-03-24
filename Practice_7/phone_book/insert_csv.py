import psycopg
from config import load_config
import csv


def insert_residence(first_name, last_name, phone_number):
    """ Insert a new residence into the  table """

    sql = """INSERT INTO residence(first_name, last_name, phone_number) VALUES(%s, %s, %s) RETURNING residence_id;"""

    residence_id = None
    config = load_config()

    try:
        with  psycopg.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (first_name, last_name, phone_number))

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    residence_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return residence_id

def insert_many_residences(residence_list):
    """ Insert multiple residences into the residences table  """

    sql = "INSERT INTO residence(first_name, last_name, phone_number) VALUES(%s, %s, %s) RETURNING *"
    config = load_config()
    try:
        with  psycopg.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.executemany(sql, residence_list)

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    with open("new_residence.csv") as file:
        reader = csv.reader(file)
        next(reader)
        rows = []
        for row in reader:
            rows.append(row)

    insert_many_residences(rows)