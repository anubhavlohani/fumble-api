from fastapi import FastAPI, HTTPException, Depends, UploadFile
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
	allow_origins=["http://localhost:3000", "https://exquisite-salamander-ca0e85.netlify.app"],
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

@app.post("/signup")
def sign_up(user: schemas.UserSignUp, db: Session = Depends(get_db)):
	existing_user = crud.get_user(db, user.username)
	if existing_user:
		raise HTTPException(status_code=409, detail='Another user with this username exists. Try logging in or use a different username.')
	try:
		user.password = helpers.generate_password_hash(user.password)
		crud.create_user(db, user)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422)
	return {'success': True}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	auth_data = helpers.authenticate_user(db, form_data)
	return auth_data

@app.post("/file-upload")
async def upload_file(image: UploadFile, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	user = helpers.decode_token(db, token)
	image_content = await image.read()
	crud.add_meme(db, user, image_content)
	return {'success': True}

@app.get('/verify-token')
def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	return {'success': True}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
