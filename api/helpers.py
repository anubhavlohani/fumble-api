from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext
import tekore as tk

from . import crud, models, schemas
from .config import SECRET_KEY, ALGORITHM



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def generate_password_hash(password) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=1440)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm) -> dict:
	user = crud.get_user(db, form_data.username)
	if not user:
		raise HTTPException(status_code=400, detail="Incorrect username or password")
	if not verify_password(form_data.password, user.password):
		raise HTTPException(status_code=400, detail="Incorrect username or password")
	
	token_data = {'username': user.username}
	access_token = create_access_token(token_data)

	return {"access_token": access_token, "token_type": "bearer"}

def decode_token(db: Session, token: str) -> models.User:
	try:
		decoded_jwt = jwt.decode(token, SECRET_KEY, ALGORITHM)
	except ExpiredSignatureError:
		raise HTTPException(status_code=440, detail="Session expired, please login again.")
	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid authentication")
	current_user = crud.get_user(db, decoded_jwt['username'])
	if current_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return current_user



'''
Spotify Helper Functions
Note: We instantiate a Spotify client (with auto-refreshing client token)
while instantiating FastApi app in main.py which is created in config.py
'''
def search_spotify(spotify: tk.Spotify, query: str) -> list[schemas.Item]:
	res = spotify.search(query=query, limit=50)
	all_tracks = res[0].items
	lowercased_track_names = []
	for track in all_tracks:
		if track.name.lower() not in lowercased_track_names:
			lowercased_track_names.append(track.name.lower())
	result = []
	for track_name in lowercased_track_names:
		track = None
		for x in all_tracks:
			if track_name == x.name.lower():
				track = x
				break
		result.append(schemas.Item(id=track.id, name=track.name))
	result = result[:10]
	return result

def artist_details(spotify: tk.Spotify, artist_id: str) -> schemas.Artist:
	artist = spotify.artist(artist_id=artist_id)
	artist = schemas.Artist(
		id=artist.id,
		name=artist.name,
		spotify_url=artist.external_urls['spotify'],
		followers=artist.followers.total,
		genres=artist.genres,
		popularity=artist.popularity,
		images=[image.url for image in artist.images]
	)
	return artist
	
def album_details(spotify: tk.Spotify, album_id: str) -> schemas.Album:
	album = spotify.album(album_id=album_id)
	album = schemas.Album(
		id=album.id,
		name=album.name,
		spotify_url=album.external_urls['spotify'],
		artists=[artist_details(spotify, artist.id) for artist in album.artists],
		images=[image.url for image in album.images],
		release_date=album.release_date
	)
	return album

def track_details(spotify: tk.Spotify, track_id: str) -> schemas.Track:
	track = spotify.track(track_id=track_id)
	artists = [artist_details(spotify, artist.id) for artist in track.artists]
	album = album_details(spotify, track.album.id)
	track = schemas.Track(
		id=track.id,
		name=track.name,
		spotify_url=track.external_urls['spotify'],
		artists=artists,
		album=album,
		preview_url=track.preview_url
	)
	return track