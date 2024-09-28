import sqlite3
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from src.db import get_db
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

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

@router.post("/", response_model=Token)
async def register_user(user: UserLogin):
    # create user object
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    user_id = len(fake_users_db) + 1

    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed_password,
        "user_id": user_id
    }
    print(fake_users_db)

    access_token = create_access_token(user_id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    user = authenticate_user(user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user["user_id"])
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(user_id: int = Depends(get_current_user)):
    return {"message": user_id}