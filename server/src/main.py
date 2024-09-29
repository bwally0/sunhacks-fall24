import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
from src.db import create_tables, DB_PATH
import src.auth

# startup event to init database
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isdir("data"):
        os.mkdir("data")
        db_con = sqlite3.connect(DB_PATH)
        db_cur = db_con.cursor()
        create_tables(db_cur)
        db_con.commit()
        db_cur.close()
        db_con.close()
    yield

app = FastAPI(root_path="/api", lifespan=lifespan)
app.include_router(src.auth.router)

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