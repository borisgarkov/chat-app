from typing import Annotated
from fastapi import FastAPI, WebSocket, Depends, HTTPException, status, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta, datetime

from db import crud, models, schemas
from db.database import engine, SessionLocal
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from tokens import create_access_token
from hashing import verify_password
from websocket_manager import ConnectionManager


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TokenData(BaseModel):
    username: str | None = None


def fake_hashed_password(password: str):
    return password + "notreallyhashed"


def raise_incorrect_username_password_error():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")


def raise_credentials_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def authenticate_user(username: str, password: str):
    user = crud.get_user_by_username(db=get_db(), username=username)
    if not user or not not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise_credentials_error()

        token_data = TokenData(username=username)
    except JWTError as e:
        print('JWTError')
        print(e)
        raise_credentials_error()
    user = crud.get_user_by_username(db=db, username=token_data.username)
    if not user:
        raise_credentials_error()
    return user


@app.post("/login/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    print(form_data)

    user_dict = crud.get_user_by_username(db, form_data.username)
    if not user_dict:
        raise_incorrect_username_password_error()

    user = schemas.UserCreate(
        username=user_dict.username, password=user_dict.hashed_password)

    if not user.password == fake_hashed_password(form_data.password):
        raise raise_incorrect_username_password_error()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user_dict.id}


@app.post("/register/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)) -> list[schemas.User]:
    return crud.get_all_users_from_db(db)


@app.get("/chat-history/")
async def get_chat_history(recipient_id: int, token: str, db: Session = Depends(get_db)):
    loggedInUser = get_current_user(token=token, db=db)
    return crud.fetch_user_messages(sender_id=loggedInUser.id, recipient_id=recipient_id, db=db)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_message(websocket: WebSocket, client_id: int,  db: Session = Depends(get_db)):
    await websocket.accept()

    token = await websocket.receive_text()
    loggedInUser = get_current_user(token=token, db=db)

    manager.add_connection(user_id=loggedInUser.id, websocket=websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = schemas.MessageCreate(
                message=data,
                sender_id=loggedInUser.id,
                recipient_id=client_id,
                timestamp=datetime.now()
            )
            crud.create_message(db=db, message_details=message)
            await manager.send_private_message(recipient_id=client_id, message=data)
    except WebSocketDisconnect:
        await manager.disconnect(user_id=loggedInUser.id)


if __name__ == "__main__":
    uvicorn.run(app="app:app", port=9000, reload=True)
