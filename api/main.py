from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
import uvicorn

from . import models, schemas, crud, helpers
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
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
		user.password = helpers.generate_password_hash(user.password)
		crud.create_user(db, user)
	except Exception as err:
		print(err)
	return {'success': True}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	auth_data = helpers.authenticate_user(db, form_data)
	return auth_data

@app.post("/uploadFile")
async def upload_file(image: UploadFile, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	user = helpers.decode_token(db, token)
	image_content = await image.read()
	crud.add_meme(db, user, image_content)
	return {'success': True}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
