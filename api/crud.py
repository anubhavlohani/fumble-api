from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, username: int) -> models.User:
	return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserSignUp) -> models.User:
	existing_user = get_user(db, user.username)
	if existing_user:
		return existing_user
	db_user = models.User(**user.dict())
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def add_meme(db: Session, user: models.User, meme: bytes) -> models.Meme:
	new_meme = models.Meme(file=meme, owner_id=user.id)
	db.add(new_meme)
	db.commit()
	db.refresh(new_meme)
	return new_meme