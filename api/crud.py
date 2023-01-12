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

def create_story(db: Session, user: models.User, story: schemas.NewStory) -> models.Story:
	story_data = story.dict()
	story_data['user_id'] = user.id
	new_story = models.Story(**story_data)
	db.add(new_story)
	db.commit()
	db.refresh(new_story)
	return new_story