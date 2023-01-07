from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return "Ahh, I see you've found this API 🦄. Welcome 🦚"

@app.get("/get-user")
def does_user_exist(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, username)
    data = {
        'found': True if user else False,
        'user': user
    }
    return data

@app.post("/signup")
def sign_up(user: schemas.UserSignUp, db: Session = Depends(get_db)):
    try:
        crud.create_user(db, user)
    except Exception as err:
        print(err)
    return {'success': True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
