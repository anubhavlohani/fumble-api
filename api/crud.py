import os
import uuid
from sqlalchemy.orm import Session

from . import models, schemas
from .config import MEME_DIR


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

def add_meme(db: Session, user: models.User, image_content: bytes, image_name: str, caption: str) -> models.Meme:
	file_ext = image_name.split('.')[-1]
	unique_file_id = '{}.{}'.format(str(uuid.uuid4()), file_ext)
	filepath = os.path.join(MEME_DIR, unique_file_id)
	with open(filepath, 'wb') as f:
		f.write(image_content)
	new_meme = models.Meme(filename=image_name, filepath=filepath, caption=caption, owner_id=user.id)
	db.add(new_meme)
	db.commit()
	db.refresh(new_meme)
	return new_meme