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

def all_stories(db: Session, spotify: tk.Spotify, requesting_user: models.User) -> list[schemas.DetailedStory]:
	stories = db.query(models.Story)
	detailed_stories = []
	for story in stories:
		track = helpers.track_details(spotify, story.track_id)
		like_records = db.query(models.Like).filter(models.Like.story_id == story.id).all()
		liked_by_user = False
		for like_record in like_records:
			if like_record.user_id == requesting_user.id:
				liked_by_user = True
				break
		detailed_story = schemas.DetailedStory(
			id=story.id,
			username=story.user.username,
			track=track,
			caption=story.caption,
			time_created=story.time_created,
			liked=liked_by_user,
			comments=story.comments
		)
		detailed_stories.append(detailed_story)
	# sort by time by default
	detailed_stories = sorted(detailed_stories, key=lambda x: x.time_created, reverse=True)
	return detailed_stories

def like_story(db: Session, like: schemas.NewLike) -> models.Like:
	like_data = like.dict()
	new_like = models.Like(**like_data)
	db.add(new_like)
	db.commit()
	db.refresh(new_like)
	return new_like

def delete_like(db: Session, like: schemas.NewLike) -> bool:
	to_delete = db.query(models.Like).filter(like.story_id == models.Like.story_id).filter(like.user_id == models.Like.user_id).first()
	if to_delete:
		db.delete(to_delete)
		db.commit()
		return True
	return False

def create_comment(db: Session, comment: schemas.NewComment) -> models.Comment:
	comment_data = comment.dict()
	new_comment = models.Comment(**comment_data)
	db.add(new_comment)
	db.commit()
	db.refresh(new_comment)
	return new_comment