import psycopg

def connect_and_test(config):
    """Connect to the PostgreSQL database server with pagination loop"""
    try:
        with psycopg.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')

            limit = int(input("Enter limit (page size): "))
            offset = 0  # start from first page

            while True:
                print(f"\n--- Page (offset={offset}) ---")

                sql = "SELECT * FROM get_paginated(%s, %s);"
                result = conn.execute(sql, (limit, offset))
                rows = result.fetchall()

                if not rows:
                    print("No more data.")
                else:
                    for row in rows:
                        print(row)

                # user navigation
                command = input("\nEnter command (next / prev / quit): ").strip().lower()

                if command == "next":
                    offset += limit

                elif command == "prev":
                    offset = max(0, offset - limit)  # prevent negative offset

                elif command == "quit":
                    print("Exiting pagination.")
                    break

                else:
                    print("Invalid command. Use next / prev / quit.")

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