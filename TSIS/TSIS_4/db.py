import psycopg
from datetime import datetime

# Connection details - Update with your local credentials
DB_PARAMS = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "damir2007",
    "host": "localhost"
}

def get_connection():
    return psycopg.connect(**DB_PARAMS)

def save_result(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    # 1. Ensure player exists and get ID
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (username,))
    cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
    player_id = cur.fetchone()[0]
    
    # 2. Insert session
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
                (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT p.username, s.score, s.level_reached, s.played_at 
        FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        ORDER BY s.score DESC LIMIT 10;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(score) FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        WHERE p.username = %s
    """, (username,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0