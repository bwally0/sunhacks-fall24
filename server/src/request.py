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
            VALUES (?, ?, ?, ?)""",
            (request.owner_id, request.workout_id, user_id, 0))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        request_id = db_cur.lastrowid
        db_cur.close()

    request = Request(request_id=request_id, owner_id=request.owner_id, workout_id=request.workout_id, participant_id=user_id, accepted=0)

    return request

def get_requests_by_participant_id(db_con: sqlite3.Connection, user_id: int) -> list[Request] | None:
    db_cur = db_con.cursor()

    requests = None

    try:
        db_cur.execute("""
            SELECT * FROM requests WHERE participant_id = ?
            """, (user_id,))
        reses = db_cur.fetchall()

        for res in reses:
            requests.append(Request(request_id=res[0], owner_id=res[1], workout_id=res[2], participant_id=res[3], accepted=res[4]))
    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return requests

def get_requests_by_owner_id(db_con: sqlite3.Connection, user_id: int) -> list[Request] | None:
    db_cur = db_con.cursor()

    requests = []

    try:
        db_cur.execute("""
            SELECT * FROM requests WHERE owner_id = ?
            """, (user_id,))
        reses = db_cur.fetchall()

        for res in reses:
            requests.append(Request(request_id=res[0], owner_id=res[1], workout_id=res[2], participant_id=res[3], accepted=res[4]))
    except sqlite3.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    return requests

# TODO implement with parameters
def get_request_by_id() -> Request | None:
    pass


def accept_request(db_con: sqlite3.Connection, request_id, owner_id) -> None:
    # verify that owner is the owner_id of the request
    # verify that the request is not already accepted
    # set accepted to 1
    # add user_id and workout_id to workout_members table
    pass