import psycopg
from config import load_config


def delete_residence(first_name):
    """ Delete residence by residence name """

    rows_deleted  = 0
    sql = 'DELETE FROM residence WHERE first_name = %s'
    config = load_config()

    try:
        with  psycopg.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the UPDATE statement
                cur.execute(sql, (first_name,))
                rows_deleted = cur.rowcount
                cur.execute("SELECT * FROM residence;")
                row = cur.fetchone()

                while row is not None:
                    print(row)
                    row = cur.fetchone()
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        return rows_deleted

if __name__ == '__main__':
    first_name = input("Enter the first name of resident that you want to delete: ")
    deleted_rows = delete_residence(first_name)
    print('The number of deleted rows: ', deleted_rows)