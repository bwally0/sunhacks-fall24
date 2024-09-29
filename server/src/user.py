import sqlite3
from fastapi import HTTPException
from typing import Any
from src.models import User, CreateUser, UpdateUser

def create_user(db_con: sqlite3.Connection, user_create: CreateUser) -> User | None:
    db_cur = db_con.cursor()

    user_create.user_id = None

    try:
        db_cur.execute("""
            INSERT INTO users (username, hashed_password, first_name, last_name, location, gender, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_create.username, user_create.hashed_password, user_create.first_name, user_create.last_name, user_create.location, user_create.gender, user_create.phone))
        db_con.commit()
    except  sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        user_create.user_id = db_cur.lastrowid
        db_cur.close

    user = User(user_id=user_create.user_id, username=user_create.username, first_name=user_create.first_name, last_name=user_create.last_name, location=user_create.location, gender=user_create.gender, phone=user_create.phone)

    return user

def update_user(db_con: sqlite3.Connection, user: UpdateUser, user_id: int) -> User | None:
    db_cur = db_con.cursor()

    try:
        db_cur.execute("""
        UPDATE users 
        SET first_name = ?, last_name = ?, location = ?, gender = ?, phone = ?
        WHERE user_id = ?
        """, (user.first_name, user.last_name, user.location, user.gender, user.phone, user_id))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return get_user(db_con, user_id)

def get_user_by_name(db_con: sqlite3.Connection, username: str) -> User | None:
    db_cur = db_con.cursor()

    user = None

    try:
        db_cur.execute("""
            SELECT * FROM users where username = ?    
        """, (username,))

        res = db_cur.fetchone()

        if res:
            user = CreateUser(user_id=res[0], username=res[1], hashed_password=res[2], first_name=res[3], last_name=res[4], location=res[5], gender=res[6], phone=res[7])
    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    finally:
        db_cur.close()

    return user


def get_user(db_con: sqlite3.Connection, user_id: int) -> User | None:     
    db_cur = db_con.cursor()

    user = None
    
    try:
        db_cur.execute("""
            SELECT * FROM users where user_id = ? 
        """, (user_id,))

        res = db_cur.fetchone()

        if res:
            user = User(user_id=res[0], username=res[1], first_name=res[3], last_name=res[4], location=res[5], gender=res[6], phone=res[7])

    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    
    finally:
        db_cur.close()
    
    return user
