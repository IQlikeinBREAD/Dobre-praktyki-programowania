from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath("../Dobre-praktyki-programowania/movies.db"))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'movies.db')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL,echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()