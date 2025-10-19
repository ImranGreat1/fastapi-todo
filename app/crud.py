from sqlalchemy.orm import Session
from .models import Task, User
from app.schemas import Task as TaskType
from .schemas import UserCreate
from fastapi import HTTPException
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token

# TASK
def create_task(db: Session, data: TaskType):
    task = Task(description=data.description, duration_min=data.duration_min, status=data.status)
    db.add(task) # Add to session
    db.commit() # Save to DB
    db.refresh(task) # get updated task with ID
    return task


def get_all_tasks(db: Session):
    tasks = db.query(Task).all()
    return tasks


def get_task_by_id(db: Session, id: int):
    task = db.query(Task).filter(Task.id == id).first()
    return task


def get_all_task(db: Session):
    tasks = db.query(Task).all()
    return tasks


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return { "message": "Task deleted successfully" }


# USER
def signup(db: Session, userData: UserCreate):
    existing_user = db.query(User).filter(User.email == userData.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists") 
    
    # Hash password
    password_hash = hash_password(userData.password)

    # Create User and save to db
    user = User(email=userData.email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate and return token
    token = create_access_token({ "email": user.email })
    return { "token": token, "token_type": "bearer", "email": user.email }


def login(db: Session, userData: UserCreate):
    # Check if user exist and verify password
    existing_user = db.query(User).filter(User.email == userData.email).first()
    if not existing_user or not verify_password(userData.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials") 
    
    # Generate and return token
    token = create_access_token({ "email": existing_user.email })
    return { "token": token, "token_type": "bearer", "email": existing_user.email }