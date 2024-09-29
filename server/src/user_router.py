import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.db import get_db
from src.models import User, CreateUser, UpdateUser
from src.auth import get_current_user
import src.user as user_db
import jwt

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.put("/", response_model=User)
def update_user(user: UpdateUser, user_id: int = Depends(get_current_user), db_con: sqlite3.Connection = Depends(get_db)):
    updated_user = user_db.update_user(db_con, user, user_id)

    return updated_user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db_con: sqlite3.Connection = Depends(get_db)):
    user = user_db.get_user(db_con, user_id)
    return user