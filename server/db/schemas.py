from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    sender_id: int
    recipient_id: int
    timestamp: datetime
    message: str
