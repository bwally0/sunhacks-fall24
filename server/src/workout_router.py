import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.db import get_db
from src.models import Workout, CreateWorkout
import jwt
from src.workout import create_workout as db_create_workout
from src.workout import update_workout as db_update_workout
from src.workout import get_workout as db_get_workout
from src.workout import get_users_owned_workouts as db_get_owned_workouts
from src.workout import get_all_workouts as db_get_all_workouts
from src.workout import remove_workout as db_delete_workout
from src.auth import get_current_user
import traceback

router = APIRouter(
    prefix='/workout',
    tags=['workout']
)

@router.post("/create", response_model=Workout)
async def create_workout(workout: CreateWorkout, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    new_workout = Workout(workout_id=0, name=workout.name, date_time=workout.date_time, tag1=workout.tag1, tag2=workout.tag2, tag3=workout.tag3, description=workout.description, location=workout.location, owner_id=user_id)

    return db_create_workout(db_con, new_workout, user_id)

@router.post("/delete/{workout_id}")
async def delete_workout(workout_id: int, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    db_delete_workout(db_con, workout_id, user_id)

@router.put("/", response_model=Workout)
async def update_workout(workout: Workout, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    return db_update_workout(db_con, workout)

@router.get("/{workout_id}", response_model=Workout)
async def get_workout(workout_id: int, db_con: sqlite3.Connection = Depends(get_db)):
    
    return db_get_workout(db_con, workout_id)

@router.get("/owned/{owner_id}", response_model=list[Workout])
async def get_owned_workouts(user_id: int = (Depends(get_current_user)), db_con: sqlite3.Connection = Depends(get_db)):
    return db_get_owned_workouts(db_con, user_id)

@router.get("/", response_model=list[Workout])
async def get_all_workouts(user_id: int = (Depends(get_current_user)), db_con: sqlite3.Connection = Depends(get_db)):
    return db_get_all_workouts(db_con, user_id)

# /workout/joined
