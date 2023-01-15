import os
import tekore as tk

curr_dir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(curr_dir, 'database.sqlite3')

ALGORITHM = "HS256"

SECRET_KEY = 'wellWellWellIfItAintTheInvisibleC*nt'

SPOTIFY_CLIENT_ID = 'dd5b0904f89e4f559c717cdf4b50e35d'
SPOTIFY_CLIENT_SECRET = '17b66e99912542e68e0e4e316a68c13a'

def get_spotify() -> tk.Spotify:
    app_token = tk.request_client_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    spotify = tk.Spotify(app_token, max_limits_on=True)
    return spotify