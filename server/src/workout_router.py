import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.db import get_db
from src.models import Workout, CreateWorkout
import jwt
from src.workout import create_workout as db_create_workout
from src.auth import get_current_user

router = APIRouter(
    prefix='/workout',
    tags=['workout']
)

@router.post("/", response_model=Workout)
async def create_workout(workout: CreateWorkout, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    new_workout = Workout(workout_id=0, name=workout.name, date_time=workout.date_time, tag1=workout.tag1, tag2=workout.tag2, tag3=workout.tag3, description=workout.description, location=workout.location, owner_id=user_id)

    return db_create_workout(db_con, new_workout)
