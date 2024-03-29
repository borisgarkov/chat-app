from passlib.context import CryptContext
from db import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def fake_hashed_password(password: str):
    return password + "notreallyhashed"
