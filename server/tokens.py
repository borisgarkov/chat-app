from pydantic import BaseModel
from datetime import timedelta, datetime
from jose import jwt
from constants import SECRET_KEY, ALGORITHM
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from custom_exceptions import raise_unauthorized_error
from db import crud


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    current_time = datetime.utcnow()

    expire = current_time + expires_delta if expires_delta else current_time + \
        timedelta(minutes=60 * 60 * 10)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise_unauthorized_error()

    except JWTError as e:
        print('JWTError')
        print(e)
        raise_unauthorized_error()
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        raise_unauthorized_error()
    return user
