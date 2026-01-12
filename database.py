import sqlite3
from pathlib import Path
import logging

DB_FILE = Path("data/countries.db")
DB_FILE.parent.mkdir(exist_ok=True)

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def connect_db():
    logging.info("Connecting to SQLite database")
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
    logging.info("Countries table created or already exists")

def insert_data(data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO countries (country, capital, population, area)
        VALUES (?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()
    logging.info(f"{len(data)} records inserted into database")