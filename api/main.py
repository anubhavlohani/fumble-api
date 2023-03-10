from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
import uvicorn

from . import models, schemas, crud, helpers
from .database import SessionLocal, engine
from .config import get_spotify

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

spotify = get_spotify()

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
		raise HTTPException(status_code=422, detail="Unable to create new user")
	return {'success': True}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	auth_data = helpers.authenticate_user(db, form_data)
	return auth_data

@app.get('/verify-token')
def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	user = helpers.decode_token(db, token)
	user_details = schemas.ReturnUser(
		id=user.id,
		username=user.username,
		name=user.name,
		email=user.email
	)
	return {'user_details': user_details}

@app.get('/search-spotify')
def search_spotify(q: str):
	search_res = helpers.search_spotify(spotify, q)
	return {'results': search_res}

@app.get('/all-stories')
def all_stories(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	user = helpers.decode_token(db, token)
	stories = crud.all_stories(db, spotify, user)
	return {'stories': stories}

@app.post('/create-story')
def create_story(story: schemas.NewStory, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	user = helpers.decode_token(db, token)
	try:
		crud.create_story(db, user, story)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to create new story")
	return {'success': True}

@app.delete('/delete-story')
def delete_story(story_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	try:
		crud.delete_story(db, story_id)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to delete story")
	return {'success': True}

@app.post('/like-story')
def like_story(like: schemas.NewLike, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	try:
		crud.like_story(db, like)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="An error occured while trying to like this story. Please try again.")
	return {'success': True}

@app.delete('/delete-like')
def unlike_story(like: schemas.NewLike, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	try:
		crud.delete_like(db, like)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="An error occured while trying to like this story. Please try again.")
	return {'success': True}

@app.get('/story-comments')
def get_comments(story_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	comments = crud.get_comments(db, story_id)
	return {'comments': comments}

@app.post('/post-comment')
def new_comment(comment: schemas.NewComment, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	try:
		crud.create_comment(db, comment)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="An error occured while trying to comment. Please try again.")
	return {'success': True}

@app.delete('/delete-comment')
def delete_comment(comment_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	helpers.decode_token(db, token)
	try:
		crud.delete_comment(db, comment_id)
	except Exception as err:
		print(err)
		raise HTTPException(status_code=422, detail="Unable to delete comment")
	return {'success': True}



if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
