from pydantic import BaseModel
from typing import Union
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
  spotify_url: str

class Artist(Item):
  followers: int
  genres: list[str]
  popularity: int
  images: list[str]

class Album(Item):
  artists: list[Artist]
  images: list[str]
  release_date: str

class Track(Item):
  artists: list[Artist]
  album: Album
  preview_url: Union[str, None]



'''
Hybrid schemas
'''
class DetailedStory(BaseModel):
  id: int
  username: str
  track: Track
  caption: str
  time_created: datetime.datetime