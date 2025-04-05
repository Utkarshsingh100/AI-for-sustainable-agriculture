import sqlite3
from datetime import datetime

DB_NAME = "db.sqlite"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT NOT NULL,
            user_input TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_interaction(agent, user_input, response):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute("""
        INSERT INTO interactions (agent, user_input, response, timestamp)
        VALUES (?, ?, ?, ?)
    """, (agent, user_input, response, timestamp))
    conn.commit()
    conn.close()

def get_interaction_history(agent=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if agent:
        c.execute("SELECT * FROM interactions WHERE agent = ? ORDER BY timestamp DESC", (agent,))
    else:
        c.execute("SELECT * FROM interactions ORDER BY timestamp DESC")
    results = c.fetchall()
    conn.close()
    return results
