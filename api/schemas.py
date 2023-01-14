from pydantic import BaseModel
import datetime


'''
ORM schemas
'''
class UserLogin(BaseModel):
  username: str
  password: str

class UserSignUp(UserLogin):
  username: str
  name: str
  password: str
  email: str

  class Config:
    orm_mode = True

class NewStory(BaseModel):
  track_id: str
  caption: str



'''
Spotify schemas
'''
class Item(BaseModel):
  id: str
  name: str

class Artist(Item):
  followers: int
  genres: list[str]
  popularity: int
  images: list[str]

class Album(Item):
  artists: list[Artist]
  images: list[str]

class Track(Item):
  artists: list[Artist]
  album: Album



'''
Hybrid schemas
'''
class DetailedStory(BaseModel):
  username: str
  track: Track
  caption: str
  time_created: datetime.datetime