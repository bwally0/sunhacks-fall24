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
            username TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            gym_loc TEXT,
            gender TEXT,
            phone TEXT
        );
        
        CREATE TABLE IF NOT EXISTS workout (
            workoutId INTEGER PRIMARY KEY,
            name TEXT,
            time TEXT,
            tag1 TEXT,
            tag2 TEXT,
            tag3 TEXT,
            desc TEXT,
            ownerId INTEGER,
            FOREIGN KEY (ownerId) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS workout_members (
            workout_id INTEGER,
            user_id INTEGER,
            PRIMARY KEY (workout_id, user_id),
            FOREIGN KEY (workout_id) REFERENCES workout(workoutId),
            FOREIGN KEY (user_id) REFERENCES user(id)
        );

        CREATE TABLE IF NOT EXISTS requests (
            ownerId INTEGER,
            workout INTEGER,
            participant INTEGER,
            accepted INTEGER
            PRIMARY KEY (ownerId, workout, participant)
            FOREIGN KEY (ownerId) REFERENCES workout(ownerId)
            FOREIGN KEY (workout) REFERENCES workout(workoutId)
            FOREIGN KEY (participant) REFERENCES user(id)
        );
    """)