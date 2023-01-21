from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String, nullable=False)
	name = Column(String, nullable=False)
	password = Column(String, nullable=False)
	email = Column(String, nullable=False)

	stories = relationship("Story", backref="user")
	comments = relationship("Comment", backref="user")


class Story(Base):
	__tablename__ = 'story'

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("user.id"), unique=False, nullable=False)
	track_id = Column(String, unique=False, nullable=False)
	caption = Column(String, unique=False, nullable=True)
	time_created = Column(DateTime, unique=False, nullable=False)

	comments = relationship("Comment", backref="story")


class Like(Base):
	__tablename__ = "like"

	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("user.id"), unique=False, nullable=False)
	story_id = Column(Integer, ForeignKey("story.id"), unique=False, nullable=False)


class Comment(Base):
	__tablename__ = "comment"

	id = Column(Integer, primary_key=True, autoincrement=True)
	content = Column(String, unique=False, nullable=False)
	user_id = Column(Integer, ForeignKey("user.id"), unique=False, nullable=False)
	story_id = Column(Integer, ForeignKey("story.id"), unique=False, nullable=False)