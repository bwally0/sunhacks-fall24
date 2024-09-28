import sqlite3
import os

DB_PATH = "data/app.db"

def get_db():
    db_con = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield db_con
    finally:
        db_con.close()

def create_tables(db_cur: sqlite3.Cursor):
    db_cur.executescript("""
        PRAGMA foreign_keys = ON;
                         
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL
        );
    """)