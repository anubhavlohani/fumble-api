import datetime

from sqlalchemy.orm import Session
import tekore as tk

from . import models, schemas, helpers


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
	story_data['time_created'] = datetime.datetime.now()
	new_story = models.Story(**story_data)
	db.add(new_story)
	db.commit()
	db.refresh(new_story)
	return new_story

def all_stories(db: Session, spotify: tk.Spotify) -> list[schemas.DetailedStory]:
	stories = db.query(models.Story)
	detailed_stories = []
	for story in stories:
		track = helpers.track_details(spotify, story.track_id)
		detailed_story = schemas.DetailedStory(
			username=story.user.username,
			track=track,
			caption=story.caption,
			time_created=story.time_created
		)
		detailed_stories.append(detailed_story)
	# sort by time by default
	detailed_stories = sorted(detailed_stories, key=lambda x: x.time_created, reverse=True)
	return detailed_stories