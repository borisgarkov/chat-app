from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_all_users_from_db(db: Session):
    """
    fetch all users from database and remove password records
    """
    query_results = db.query(models.User).all()
    return [{"username": q.username, "id": q.id} for q in query_results]


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_message(db: Session, message_details: schemas.MessageCreate):
    new_message = models.Message(
        message=message_details.message,
        sender_id=message_details.sender_id,
        recipient_id=message_details.recipient_id,
        timestamp=message_details.timestamp
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def fetch_user_messages(sender_id: int, recipient_id: int, db: Session):
    return db.query(models.Message).filter(
        ((models.Message.sender_id == sender_id)
         & (models.Message.recipient_id == recipient_id))
        | ((models.Message.sender_id == recipient_id)
           & (models.Message.recipient_id == sender_id))
    ).all()


def fetch_unread_messsages(recipient_id: int, db: Session):
    return db.query(models.Message).filter(
        (models.Message.recipient_id == recipient_id)
        & (models.Message.is_message_read == False)
    ).all()
