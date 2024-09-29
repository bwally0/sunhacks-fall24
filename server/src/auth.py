import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.models import User, CreateUser
from src.db import get_db
import src.user as user_db
import jwt

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "test-key"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(UserLogin):
    first_name: str
    last_name: str
    location: str
    gender: str
    phone: str

class Token(BaseModel):
    access_token: str
    token_type: str

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": bcrypt_context.hash("testpassword"),  # Hashed password
        "user_id": 1
    }
}

def hash_password(password: str):
    return bcrypt_context.hash(password)

def verify_password(password_plain: str, password_hashed: str):
    return bcrypt_context.verify(password_plain, password_hashed)

def create_access_token(user_id: dict):
    payload = {
        "user_id": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise Exception()
    return user_id

def authenticate_user(username: str, password: str, db_con: sqlite3.Connection):
    user = user_db.get_user_by_name(db_con, username)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def test_register_user(user: UserRegister, db_con: sqlite3.Connection):
    hashed_password = hash_password(user.password)
    user = user_db.create_user(db_con, CreateUser(user_id=0, username=user.username, hashed_password=hashed_password, first_name=user.first_name, last_name=user.last_name, location=user.location, gender=user.gender, phone=user.phone))

@router.post("/", response_model=Token)
async def register_user(user: UserRegister, db_con: sqlite3.Connection = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user = user_db.create_user(db_con, CreateUser(user_id=0, username=user.username, hashed_password=hashed_password, first_name=user.first_name, last_name=user.last_name, location=user.location, gender=user.gender, phone=user.phone))

    access_token = create_access_token(user.user_id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db_con: sqlite3.Connection = Depends(get_db)):
    user = authenticate_user(user.username, user.password, db_con)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.user_id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(user_id: int = Depends(get_current_user)):
    return {"message": user_id}