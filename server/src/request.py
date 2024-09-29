import sqlite3
from fastapi import HTTPException
from typing import Any
from src.models import Request, CreateRequest

def create_request(db_con: sqlite3.Connection, request: CreateRequest, user_id: int) -> Request | None:
    db_cur = db_con.cursor()

    request_id = None

    try:
        db_cur.execute("""
            INSERT INTO requests (owner_id, workout_id, participant_id, accepted)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM requests WHERE owner_id = ? AND workout_id = ? AND participant_id = ?
            );""",
            (request.owner_id, request.workout_id, user_id, 0, request.owner_id, request.workout_id, user_id))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        request_id = db_cur.lastrowid
        db_cur.close()

    request = Request(request_id=request_id, owner_id=request.owner_id, workout_id=request.workout_id, participant_id=user_id, accepted=0)

    return request

def delete_request(db_con: sqlite3.Connection, request_id: int, user_id: int) -> None:
    db_cur = db_con.cursor()

    try:
        db_cur.execute("""
            DELETE FROM requests WHERE request_id = ? AND participant_id = ?
            """, (request_id, user_id))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

def get_requests_by_participant_id(db_con: sqlite3.Connection, user_id: int) -> list[Request] | None:
    db_cur = db_con.cursor()

    requests = []

    try:
        db_cur.execute("""
            SELECT * FROM requests WHERE participant_id = ?
            """, (user_id,))
        reses = db_cur.fetchall()

        for res in reses:
            request = Request(request_id=res[0], owner_id=res[1], workout_id=res[2], participant_id=res[3], accepted=res[4])
            requests.append(request)
    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return requests

def get_requests_by_owner_id(db_con: sqlite3.Connection, owner_id: int) -> list[Request] | None:
    db_cur = db_con.cursor()

    requests = []

    try:
        db_cur.execute("""
            SELECT * FROM requests WHERE owner_id = ?
            """, (owner_id,))
        reses = db_cur.fetchall()

        for res in reses:
            request = Request(request_id=res[0], owner_id=res[1], workout_id=res[2], participant_id=res[3], accepted=res[4])
            requests.append(request)  

    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return requests

def get_requests_by_workout_id(db_con: sqlite3.Connection, workout_id: int) -> list[Request] | None:
    db_cur = db_con.cursor()

    requests = []

    try:
        db_cur.execute("""
            SELECT * FROM requests WHERE workout_id = ?
            """, (workout_id,))
        reses = db_cur.fetchall()

        for res in reses:
            request = Request(request_id=res[0], owner_id=res[1], workout_id=res[2], participant_id=res[3], accepted=res[4])
            requests.append(request)  

    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return requests

def get_request_by_id(db_con: sqlite3.Connection, request_id: int) -> Request | None:
    db_cur = db_con.cursor()

    request = None
    
    try: 
        db_cur.execute("""
            SELECT * FROM requests WHERE request_id = ?
            """, (request_id,))
        
        res = db_cur.fetchone()

        if res:
            request = Request(request_id=res[0], owner_id=res[1], workout_id=res[2], participant_id=res[3], accepted=res[4])

    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return request


def accept_request(db_con: sqlite3.Connection, request_id: int, user_id: int) -> None:
    db_cur = db_con.cursor()

    try:
        db_cur.execute("""
            UPDATE requests 
            SET accepted = 1 WHERE request_id = ? AND owner_id = ?
            """, (request_id, user_id))
        
        workout = get_request_by_id(db_con, request_id)

        db_cur.execute("""
            INSERT INTO workout_members (workout_id, user_id)
            SELECT ?, ?
            WHERE EXISTS (
                SELECT 1 
                FROM requests
                WHERE request_id = ? AND accepted = 1
            )
            """, (workout.workout_id, user_id, request_id))
        
        db_con.commit()
        
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()
