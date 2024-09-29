import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.db import get_db
from src.models import Workout
import jwt
from src.workout import create_workout as db_create_workout
from src.auth import get_current_user

router = APIRouter(
    prefix='/workout',
    tags=['workout']
)

@router.post("/", response_model=Workout)
async def create_workout(workout: Workout, user_id: int = Depends(get_current_user)):
    
    return {}