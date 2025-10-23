from pydantic import BaseModel, EmailStr, Field
from .models import TaskStatus


class Task(BaseModel):
    description: str
    status: TaskStatus = TaskStatus.NOT_STARTED
    duration_min: int
    user_id: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3)


class TokenResponse(BaseModel):
    token: str
    token_type: str
    email: str
    user_id: int


class TokenPayload(BaseModel):
    email: str
    exp: int
