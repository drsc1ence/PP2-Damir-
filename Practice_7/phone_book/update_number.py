import psycopg
from config import load_config


def update_residence(residence_id, residence_number):
    """ Update residence name based on the residence id """

    updated_row_count = 0

    sql = """ UPDATE residence
                SET phone_number = %s
                WHERE residence_id = %s;"""

    config = load_config()

    try:
        with  psycopg.connect(**config) as conn:
            with  conn.cursor() as cur:

                # execute the UPDATE statement
                cur.execute(sql, (residence_number, residence_id))
                updated_row_count = cur.rowcount

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return updated_row_count

if __name__ == '__main__':
    residence_id = input("Enter the residence id: ")
    residence_number = input("Emter phone number: ")
    update_residence(residence_id, residence_number)