from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .models import Base
from .database import engine, get_db
from . import crud
from .schemas import Task as TaskType, TokenResponse, UserCreate


app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def get_root():
    return { "greeting": "Hello world. API works fine 🎉" }


# Create task
@app.post("/create-task")
async def create_task(task_data: TaskType, db: Session = Depends(get_db)):
    task = crud.create_task(db, task_data)
    return task


# Get all tasks
@app.get("/tasks")
async def get_all_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)


# Get task by Id
@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    return task


# Delete a task
@app.delete("/delete-task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        return { "message": f"Task with the ID of {task_id} does not exists" }
    
    message = crud.delete_task(db, task)
    return message
    

# AUTHENTICATION ROUTES

# Signup
@app.post("/signup", response_model=TokenResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    token = crud.signup(db, user)
    return token


# Login
@app.post("/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = crud.login(db, user)
    return token



