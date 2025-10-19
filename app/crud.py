from sqlalchemy.orm import Session
from .models import Task
from app.types import Task as TaskType


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