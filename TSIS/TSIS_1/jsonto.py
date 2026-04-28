import json
import psycopg

def export_to_json(conn, filename="contacts.json"):
    query = """
    SELECT r.residence_id, r.first_name, r.last_name, r.email, r.birthday,
           g.name as group_name,
           p.phone, p.type
    FROM residence r
    LEFT JOIN groups g ON r.group_id = g.id
    LEFT JOIN phones p ON r.residence_id = p.residence_id
    ORDER BY r.residence_id;
    """

    result = conn.execute(query)
    rows = result.fetchall()

    contacts = {}
    
    for row in rows:
        rid = row[0]
        if rid not in contacts:
            contacts[rid] = {
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "birthday": str(row[4]),
                "group": row[5],
                "phones": []
            }

        if row[6]:
            contacts[rid]["phones"].append({
                "number": row[6],
                "type": row[7]
            })

    with open(filename, "w") as f:
        json.dump(list(contacts.values()), f, indent=4)

    print("Exported to", filename)