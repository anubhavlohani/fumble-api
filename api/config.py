import os

curr_dir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(curr_dir, 'database.sqlite3')

SECRET_KEY = 'wellWellWellIfItAintTheInvisibleC*nt'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440