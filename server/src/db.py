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
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            location TEXT,
            gender TEXT,
            phone TEXT
        );
        
        CREATE TABLE IF NOT EXISTS workout (
            workout_id INTEGER PRIMARY KEY,
            name TEXT,
            date_time TEXT,
            tag1 TEXT,
            tag2 TEXT,
            tag3 TEXT,
            description TEXT,
            location TEXT,
            owner_id INTEGER,
            FOREIGN KEY (owner_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS workout_members (
            workout_id INTEGER,
            user_id INTEGER,
            PRIMARY KEY (workout_id, user_id),
            FOREIGN KEY (workout_id) REFERENCES workout(workout_id),
            FOREIGN KEY (user_id) REFERENCES user(user_id)
        );

        CREATE TABLE IF NOT EXISTS requests (
            request_id INTEGER PRIMARY KEY,
            owner_id INTEGER,
            workout_id INTEGER,
            participant_id INTEGER,
            accepted INTEGER,
            FOREIGN KEY (owner_id) REFERENCES workout(owner_id)
            FOREIGN KEY (workout_id) REFERENCES workout(workout_id)
            FOREIGN KEY (participant_id) REFERENCES user(user_id)
        );
    """)