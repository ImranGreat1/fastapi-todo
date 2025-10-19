from pydantic import BaseModel
from .models import TaskStatus


class Task(BaseModel):
    description: str
    status: TaskStatus = TaskStatus.NOT_STARTED
    duration_min: int



