from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: str
    first_name: str
    last_name: str
    loc: str
    gender: str
    phone: str

class CreateUser(User):
    hashed_password: str

class Workout(BaseModel):
    workout_id: str
    name: str
    time: str
    tag1: str
    tag2: str
    tag3: str
    desc: str
    loc: str
    owner_id: int

class Request(BaseModel):
    owner_id: int
    workout: int
    participant: int
    accepted: int

