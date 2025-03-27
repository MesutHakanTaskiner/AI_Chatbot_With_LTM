import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table for user details with required fields and auto-increment id
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dates TEXT,
            profession TEXT,
            location TEXT,
            preferences TEXT,
            personal_details TEXT,
            goals TEXT,
            special_details TEXT
        )
    """)

    # Create table for embeddings with a foreign key referencing user_details id
    cur.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name blob,
            dates blob,
            profession blob,
            location blob,
            preferences blob,
            personal_details blob,
            goals blob,
            special_details blob,
            FOREIGN KEY (user_id) REFERENCES user_details(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
