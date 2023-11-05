from typing import Annotated
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from sqlalchemy.orm import Session

from datetime import timedelta, datetime

from db import crud, models, schemas
from db.database import engine, get_db
from constants import ACCESS_TOKEN_EXPIRE_SECONDS
from websocket_manager import ConnectionManager
from tokens import authenticate_user, create_access_token
from custom_exceptions import raise_unauthorized_error, raise_incorrect_username_password_error, raise_username_already_taken
from hashing import fake_hashed_password


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


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

websocket_manager = ConnectionManager()


@app.post("/login/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db),
):
    user_dict = crud.get_user_by_username(db, form_data.username)
    if not user_dict:
        raise_incorrect_username_password_error()

    user = schemas.UserCreate(
        username=user_dict.username, password=user_dict.hashed_password)

    if not user.password == fake_hashed_password(form_data.password):
        raise raise_incorrect_username_password_error()

    access_token_expires = timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,
        max_age=ACCESS_TOKEN_EXPIRE_SECONDS
    )

    return {"user_id": user_dict.id}


@app.post("/register/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise_username_already_taken()

    registered_user = crud.create_user(db=db, user=user)
    return {"user_id": registered_user.id}


@app.get("/users/")
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    access_token: Annotated[str | None, Cookie()] = None,
) -> list[schemas.User]:

    if access_token is None:
        raise_unauthorized_error()

    authenticate_user(token=access_token, db=db)

    return crud.get_all_users_from_db(db)


@app.get("/chat-history/")
def get_chat_history(
    recipient_id: Annotated[int, 'current logged in user id'],
    db: Annotated[Session, Depends(get_db)],
    access_token: Annotated[str | None, Cookie()] = None,
):
    loggedInUser = authenticate_user(token=access_token, db=db)
    return crud.fetch_user_messages(sender_id=loggedInUser.id, recipient_id=recipient_id, db=db)


@app.websocket("/unread-messages/{client_id}")
async def get_unread_messages(websocket: WebSocket, client_id: int,  db: Session = Depends(get_db)):
    await websocket.accept()

    unread_messages_array = crud.fetch_unread_messsages(
        recipient_id=client_id, db=db)

    return {"number_of_unread_messages": len([])}


@app.websocket("/ws/{client_id}")
async def websocket_message(websocket: WebSocket, client_id: int,  db: Session = Depends(get_db)):
    await websocket.accept()

    token = await websocket.receive_text()
    loggedInUser = authenticate_user(token=token, db=db)

    websocket_manager.add_connection(
        user_id=loggedInUser.id, websocket=websocket)

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
            await websocket_manager.send_private_message(recipient_id=client_id, message=data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect(user_id=loggedInUser.id)


if __name__ == "__main__":
    uvicorn.run(app="app:app", port=9000, reload=True)
