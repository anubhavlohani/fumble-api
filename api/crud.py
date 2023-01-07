from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from . import models, schemas


def get_user(db: Session, username: int):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserSignUp) -> models.User:
    existing_user = get_user(db, user.username)
    if existing_user:
        return existing_user
    hashed_password = generate_password_hash(user.password, 'sha256')
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
