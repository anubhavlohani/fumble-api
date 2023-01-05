from pydantic import BaseModel


class UserSignUp(BaseModel):
    id: int
    username: str
    name: str
    password: str
    email: str

    class Config:
      orm_mode = True