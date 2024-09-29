import os
import sqlite3
import random
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
from src.models import CreateWorkout
from src.workout import test_create_workout

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

        for workout in test_workouts:
            new_workout = CreateWorkout(**workout)
            test_create_workout(db_con, new_workout, random.randint(1, 5))

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

test_workouts = [
    {
        "name": "Morning Yoga",
        "date_time": "2024-09-28 07:00:00",
        "tag1": "Yoga",
        "tag2": "Flexibility",
        "tag3": "Relaxation",
        "description": "A relaxing morning yoga session to improve flexibility and reduce stress.",
        "location": "SDFC Tempe"
    },
    {
        "name": "HIIT Workout",
        "date_time": "2024-09-28 09:00:00",
        "tag1": "HIIT",
        "tag2": "Cardio",
        "tag3": "Strength",
        "description": "High-Intensity Interval Training (HIIT) session for burning fat and building strength.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Strength Training",
        "date_time": "2024-09-28 11:00:00",
        "tag1": "Strength",
        "tag2": "Weightlifting",
        "tag3": "Power",
        "description": "Focus on building muscle and power with heavy lifting exercises.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Zumba Dance",
        "date_time": "2024-09-28 14:00:00",
        "tag1": "Dance",
        "tag2": "Cardio",
        "tag3": "Fun",
        "description": "An energetic Zumba dance class to improve cardio while having fun.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Cycling Class",
        "date_time": "2024-09-28 16:00:00",
        "tag1": "Cycling",
        "tag2": "Endurance",
        "tag3": "Cardio",
        "description": "An intense cycling workout designed to build endurance and burn calories.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Pilates Core",
        "date_time": "2024-09-28 18:00:00",
        "tag1": "Pilates",
        "tag2": "Core",
        "tag3": "Strength",
        "description": "A Pilates session focused on strengthening the core and improving posture.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Evening Meditation",
        "date_time": "2024-09-28 19:30:00",
        "tag1": "Meditation",
        "tag2": "Mindfulness",
        "tag3": "Relaxation",
        "description": "A peaceful meditation session to wind down and clear your mind after a long day.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Functional Fitness",
        "date_time": "2024-09-29 08:00:00",
        "tag1": "Functional",
        "tag2": "Strength",
        "tag3": "Mobility",
        "description": "A functional fitness workout aimed at improving everyday movement and mobility.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Swimming Drills",
        "date_time": "2024-09-29 10:00:00",
        "tag1": "Swimming",
        "tag2": "Endurance",
        "tag3": "Technique",
        "description": "Swimming drills focused on building endurance and improving technique.",
        "location": "SDFC Tempe"
    },
    {
        "name": "Boxing Conditioning",
        "date_time": "2024-09-29 12:00:00",
        "tag1": "Boxing",
        "tag2": "Conditioning",
        "tag3": "Strength",
        "description": "A boxing-based conditioning workout for cardio, agility, and strength.",
        "location": "SDFC Tempe"
    }
]
