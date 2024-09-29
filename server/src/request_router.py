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
from fastapi import HTTPException
from typing import Any
from src.models import Request, CreateRequest
from src.request import create_request as db_create_request

router = APIRouter(
    prefix='/request',
    tags=['request']
)

@router.post("/", response_model=Request)
async def create_request(request: CreateRequest, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    new_request = CreateRequest(owner_id=request.owner_id, workout_id=request.workout_id)
    return db_create_request(db_con, new_request, user_id)