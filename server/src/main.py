import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
from src.db import create_tables, DB_PATH
import src.auth
import src.workout_router
import src.user_router
import src.request_router
from src.auth import test_register_user, UserRegister

# startup event to init database
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isdir("data"):
        os.mkdir("data")
        db_con = sqlite3.connect(DB_PATH)
        db_cur = db_con.cursor()
        create_tables(db_cur)
        db_con.commit()

        for user in test_data:
            test_user = UserRegister(**user)
            test_register_user(test_user, db_con)

        db_cur.close()
        db_con.close()
    yield

app = FastAPI(root_path="/api", lifespan=lifespan)
app.include_router(src.auth.router)
app.include_router(src.workout_router.router)
app.include_router(src.user_router.router)
app.include_router(src.request_router.router)

origins = [
    "http://localhost:5173",  # react app on port 5173
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def get_message():
    return {"message": "sunhacks fall 2024"}

test_data = [
    {
        "username": "user1",
        "password": "pass1",
        "first_name": "John",
        "last_name": "Doe",
        "location": "SDFC Tempe",
        "gender": "Male",
        "phone": "555-1234"
    },
    {
        "username": "user2",
        "password": "pass2",
        "first_name": "Jane",
        "last_name": "Smith",
        "location": "SDFC Tempe",
        "gender": "Female",
        "phone": "555-5678"
    },
    {
        "username": "user3",
        "password": "pass3",
        "first_name": "Mike",
        "last_name": "Johnson",
        "location": "SDFC Tempe",
        "gender": "Male",
        "phone": "555-8765"
    },
    {
        "username": "user4",
        "password": "pass4",
        "first_name": "Emily",
        "last_name": "Brown",
        "location": "SDFC Tempe",
        "gender": "Female",
        "phone": "555-4321"
    },
    {
        "username": "user5",
        "password": "pass5",
        "first_name": "Chris",
        "last_name": "Davis",
        "location": "SDFC Tempe",
        "gender": "Male",
        "phone": "555-1111"
    }
]