from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    location: str
    gender: str
    phone: str

class CreateUser(User):
    hashed_password: str

class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    location: str
    gender: str
    phone: str

class Workout(BaseModel):
    workout_id: int
    name: str
    date_time: str
    tag1: str
    tag2: str
    tag3: str
    description: str
    location: str
    owner_id: int

class CreateWorkout(BaseModel):
    name: str
    date_time: str
    tag1: str
    tag2: str
    tag3: str
    description: str
    location: str

class Request(BaseModel):
    owner_id: int
    workout: int
    participant: int
    accepted: int

