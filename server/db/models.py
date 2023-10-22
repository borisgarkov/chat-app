from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,)
    hashed_password = Column(String)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer,)
    recipient_id = Column(Integer,)
    timestamp = Column(DateTime,)
    message = Column(String,)
    is_message_read = Column(Boolean, default=False)
