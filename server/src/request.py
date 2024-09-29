import sqlite3
from fastapi import HTTPException
from typing import Any
from src.models import Request

def create_request(db_con: sqlite3.Connection, request: Request) -> Request | None:
    db_cur = db_con.cursor()

    try:
        db_cur.execute("""
            INSERT INTO requests (owner_id, workout, participant, accepted)
            VALUES (?, ?, ?, ?)""",
            (request.owner_id, request.workout, request.participant, request.accepted))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        request.owner_id = db_cur.lastrowid

    return request

def update_request(db_con: sqlite3.Connection, request: Request) -> Request | None:
    db_cur = db_con.cursor()

    try:
        db_cur.execute("""
            UPDATE requests
            SET owner_id = ?, workout = ?, participant = ?, accepted = ?
            WHERE owner_id = ? AND workout = ? AND participant = ?
            """, (request.owner_id, request.workout, request.participant, request.accepted))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return get_request(db_con, request.owner_id, request.workout, request.participant)

def get_request(db_con: sqlite3.Connection, owner_id: int, workout: int, participant: int) -> Request | None:
    db_cur = db_con.cursor()

    request = None

    try:
        db_cur.execute("""
            SELECT * FROM requests WHERE owner_id = ? AND workout = ? AND participant = ?
            """, (owner_id, workout, participant))
        res = db_cur.fetchone()

        if res:
            request = Request(owner_id=res[0], workout=res[1], participant=res[2], accepted=res[3])
    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return request