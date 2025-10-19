from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .models import Base, Task
from .database import engine, get_db
from . import crud
from .types import Task as TaskType


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
    return db.query(Task).all()


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
    
    



