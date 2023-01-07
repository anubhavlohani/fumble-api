from pydantic import BaseModel


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