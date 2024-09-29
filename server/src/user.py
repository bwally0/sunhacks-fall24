import sqlite3
from fastapi import HTTPException
from typing import Any
from src.models import User, CreateUser

def create_user(db_con: sqlite3.Connection, user_create: CreateUser) -> User | None:
    db_cur = db_con.cursor()

    user_create.user_id = None

    try:
        db_cur.execute("""
            INSERT INTO users (username, hashed_password, first_name, last_name, gym_loc, gender, phone)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (user_create.user_id, user_create.hashed_password, user_create.first_name, user_create.last_name, user_create.loc, user_create.gender, user_create.phone))
        db_con.commit()
    except  sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        user_create.user_id = db_cur.lastrowid

    user = User(user_id=user_create.user_id, first_name=user_create.first_name, last_name=user_create.last_name, gym_loc=user_create.loc, gender=user_create.gender, phone=user_create.phone)

    return user

def update_user(db_con: sqlite3.Connection, user: User) -> User | None:
    db_cur = db_con.cursor()

    try:
        ("""
        UPDATE users 
        SET username = ?, first_name = ?, last_name = ?, gym_loc = ?, gender = ?, phone = ?
        WHERE user_id = ?
        """, (user.username, user.first_name, user.last_name, user.loc, user.gender, user.phone, user.user_id))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return get_user(db_con, user.user_id)

def get_user(db_con: sqlite3.Connection, id: int) -> User | None:     
    db_cur = db_con.cursor()

    user = None
    
    try:
        db_cur.execute("""
            SELECT * FROM users where id = ? 
        """, (id,))

        res = db_cur.fetchone()

        if res:
            user = User(user_id=res[0], username=res[1], first_name=res[3], last_name=res[4], gym_loc=res[5], gender=res[6], phone=res[7])

    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    finally:
        db_cur.close()
    
    return user
