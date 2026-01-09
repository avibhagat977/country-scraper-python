import sqlite3
from pathlib import Path

DB_FILE = Path("data/countries.db")


def connect_db():
    return sqlite3.connect(DB_FILE)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT,
            capital TEXT,
            population INTEGER,
            area REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_data(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO countries (country, capital, population, area)
        VALUES (?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()