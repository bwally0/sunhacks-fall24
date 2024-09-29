import sqlite3
from fastapi import HTTPException
from typing import Any
from src.models import Workout
import traceback

def create_workout(db_con: sqlite3.Connection, workout: Workout) -> Workout | None:
    db_cur = db_con.cursor()

    workout.workout_id = None

    try: 
        db_cur.execute("""
            INSERT INTO workout (name, date_time, tag1, tag2, tag3, description, location, owner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (workout.name, workout.date_time, workout.tag1, workout.tag2, workout.tag3, workout.description, workout.location, workout.owner_id))
        db_con.commit()
    except sqlite3.Error as err:
        db_con.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        workout.workout_id = db_cur.lastrowid
    
    workout = Workout(workout_id=workout.workout_id, name=workout.name, date_time=workout.date_time, tag1=workout.tag1, tag2=workout.tag2, tag3=workout.tag3, description=workout.description, location=workout.location, owner_id=workout.owner_id)
    
    return workout

def update_workout(db_con: sqlite3.Connection, workout: Workout) -> Workout | None:
    db_cur = db_con.cursor()

    try: 
        ("""
        UPDATE workout
        SET name = ?, date_time = ?, tag1 = ?, tag2 = ?, tag3 = ?, description = ?, location = ?, owner_id = ?
        WHERE workout_id = ?
        """, (workout.name, workout.date_time, workout.tag1, workout.tag2, workout.tag3, workout.description, workout.location, workout.owner_id, workout.workout_id))
    except sqlite3.Error as err:
        db_con.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db_cur.close()

    updated_workout = get_workout(db_con, workout.workout_id)
    
    print(workout.workout_id)

    if not updated_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    return get_workout(db_con, workout.workout_id)   

def get_workout(db_con: sqlite3.Connection, workout_id: int) -> Workout | None:
    db_cur = db_con.cursor()

    workout = None

    try: 
        db_cur.execute(""" 
            SELECT * FROM workout WHERE workout_id = ?
            """, (workout_id,))
        
        res = db_cur.fetchone()

        if res:
            workout = Workout(workout_id=res[0], name=res[1], date_time=res[2], tag1=res[3], tag2=res[4], tag3=res[5], description=res[6], location=res[7], owner_id=res[8])
    
    except sqlite3.Error as err:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(err))
    
    finally:
        db_cur.close()
    
    return workout