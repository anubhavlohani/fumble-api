from pydantic import BaseModel


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


'''
Spotify schemas
'''
class Image(BaseModel):
  url: str

class Item(BaseModel):
  id: str
  name: str

class Artist(Item):
  popularity: int
  images: list[Image]

class Album(Item):
  artists: list[Artist]
  images: list[Image]

class Track(Item):
  name: str
  artists: list[Artist]
  album: Album