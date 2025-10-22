from typing import Union
from fastapi import FastAPI, Depends
from python_api.dbRecznie.movie import  loadMovies
from python_api.dbRecznie.links import loadLinks
from python_api.dbRecznie.ratings import loadRatings
from python_api.dbRecznie.tags import loadTags
from python_api.sql.DBSQLite import SessionLocal
from sqlalchemy.orm import Session
from python_api.sql.models import Movie, Link, Rating, Tag

app = FastAPI()

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/movies")
def get_movies(db: Session = Depends(getDB)):
    movies = db.query(Movie).all()
    return [m.__dict__ for m in movies]

@app.get("/links")
def get_links(db: Session = Depends(getDB)):
    links = db.query(Link).all()
    return links

@app.get("/ratings")
def get_ratings(db: Session = Depends(getDB)):
    ratings = db.query(Rating).all()
    return ratings

@app.get("/tags")
def get_tags(db: Session = Depends(getDB)):
    tags = db.query(Tag).all()
    return tags
