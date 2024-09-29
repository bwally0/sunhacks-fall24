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
from src.request import get_requests_by_participant_id as db_get_requests_by_participant_id
from src.request import get_requests_by_owner_id as db_get_requests_by_owner_id
from src.request import get_requests_by_workout_id as db_get_requests_by_workout_id
from src.request import delete_request as db_delete_request
from src.request import get_request_by_id as db_get_request_by_id
from src.request import accept_request as db_accept_request

router = APIRouter(
    prefix='/request',
    tags=['request']
)

@router.post("/", response_model=Request)
async def create_request(request: CreateRequest, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    new_request = CreateRequest(owner_id=request.owner_id, workout_id=request.workout_id)
    return db_create_request(db_con, new_request, user_id)

@router.get("/user", response_model=list[Request])
async def get_requests_by_participant_id(user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    return db_get_requests_by_participant_id(db_con, user_id)

@router.get("/owner", response_model=list[Request])
async def get_requests_by_owner_id(owner_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    return db_get_requests_by_owner_id(db_con, owner_id)

@router.get("/{request_id}", response_model=Request)
async def get_request_by_id(request_id: int, db_con: sqlite3.Connection = Depends(get_db)):
    return db_get_request_by_id(db_con, request_id)

@router.get("/workout/{workout_id}", response_model=list[Request])
async def get_requests_by_workout_id(workout_id: int, db_con: sqlite3.Connection = Depends(get_db)):
    return db_get_requests_by_workout_id(db_con, workout_id)

@router.put("/delete/{request_id}")
async def delete_request(request_id: int, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    db_delete_request(db_con, request_id, user_id)

@router.post("/accept/{request_id}")
async def accept_request(request_id: int, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    db_accept_request(db_con, request_id, user_id)


