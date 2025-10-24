from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import Base
from .database import engine, get_db
from . import crud
from .schemas import Task as TaskType, TokenResponse, UserCreate
from app.auth.jwt_handler import verify_access_token


app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/")
def get_root():
    return { "greeting": "Hello World. Welcome to FastAPI todo app 🎉" }


# Create task
@app.post("/tasks", dependencies=[Depends(crud.verify_token_middleware)])
async def create_task(task_data: TaskType, request: Request, db: Session = Depends(get_db)):
    task = crud.create_task(db, task_data, request["state"]["user"]["user_id"])
    return task


# Get all tasks
@app.get("/tasks", dependencies=[Depends(crud.verify_token_middleware)])
async def get_all_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db)


@app.get("/tasks/user", dependencies=[Depends(crud.verify_token_middleware)])
async def get_all_tasks_by_user(request: Request, db: Session = Depends(get_db)):
    return crud.get_all_tasks_by_user(db, request["state"]["user"]["user_id"])


# Get task by Id
@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task_by_id(db, task_id)
    return task


# Delete a task
@app.delete("/tasks/{task_id}", dependencies=[Depends(crud.verify_token_middleware)])
def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):    
    message = crud.delete_task(db, task_id, request["state"]["user"]["user_id"])
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


# Protected routes
@app.get("/profile", dependencies=[Depends(crud.verify_token_middleware)])
def get_profile(token: str = Depends(oauth2_scheme)):
    profile = crud.profile(token)
    return profile


