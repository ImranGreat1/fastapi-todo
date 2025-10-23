from sqlalchemy import Column, String, Integer, Enum, ForeignKey
import enum
from .database import Base

'''
    Note that when you query using raw SQL, you use the Enum member attribute name not the value
    e.g SELECT * task WHERE status=NOT_STARTED
'''
class TaskStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


# TASK
class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, index=True)
    duration_min = Column(Integer, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED)


# USER
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
