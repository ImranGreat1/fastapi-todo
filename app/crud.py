from sqlalchemy.orm import Session
from jose import jwt, JWTError
from .models import Task, User
from app.schemas import Task as TaskType
from .schemas import UserCreate, TokenPayload
from fastapi import HTTPException, status, Request
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token, verify_access_token
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# TASK
def create_task(db: Session, data: TaskType, user_id: int):
    task = Task(description=data.description, duration_min=data.duration_min, status=data.status, user_id=user_id)
    db.add(task) # Add to session
    db.commit() # Save to DB
    db.refresh(task) # get updated task with ID
    return task


def get_all_tasks_by_user(db: Session, user_id: int):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


def get_all_tasks(db: Session):
    tasks = db.query(Task).all()
    return tasks


def get_task_by_id(db: Session, id: int):
    task = db.query(Task).filter(Task.id == id).first()
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exists")
    
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access denied - You can't delete another person's task")

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
    token = create_access_token({ "email": user.email, "user_id": existing_user.id })
    return { "token": token, "token_type": "bearer", "email": user.email }


def login(db: Session, userData: UserCreate):
    # Check if user exist and verify password
    existing_user = db.query(User).filter(User.email == userData.email).first()
    if not existing_user or not verify_password(userData.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials") 
    
    # Generate and return token
    token = create_access_token({ "email": existing_user.email, "user_id": existing_user.id })
    return { "token": token, "token_type": "bearer", "email": existing_user.email }


def profile(token: str):
    payload: TokenPayload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    return { "message": "You are authorized", "email": payload["email"] }


def verify_token_middleware(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Optionally attach user info to request.state
        print(payload)
        request.state.user = payload
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
