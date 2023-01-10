from sqlalchemy import Column, Integer, String, ForeignKey
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

	memes = relationship("Meme", backref="owner")

class Meme(Base):
	__tablename__ = 'meme'

	id = Column(Integer, primary_key=True, autoincrement=True)
	filename = Column(String, unique=False, nullable=False)
	caption = Column(String, unique=False, nullable=True)
	filepath = Column(String, unique=True, nullable=False)
	owner_id = Column(Integer, ForeignKey("user.id"))
