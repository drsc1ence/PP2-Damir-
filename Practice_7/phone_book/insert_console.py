import psycopg
from config import load_config


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
    first_name = input("Enter the first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")
    insert_residence(first_name, last_name, phone_number)

    # insert_many_residences([
    #     ('AKM Semiconductor Inc.',),
    #     ('Asahi Glass Co Ltd.',),
    #     ('Daikin Industries Ltd.',),
    #     ('Dynacast International Inc.',),
    #     ('Foster Electric Co. Ltd.',),
    #     ('Murata Manufacturing Co. Ltd.',)
    # ])