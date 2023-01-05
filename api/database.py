import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



curr_dir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(curr_dir, 'database.sqlite3')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
