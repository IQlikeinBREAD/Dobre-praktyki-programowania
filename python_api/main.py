from typing import Union
from fastapi import FastAPI
from movie import  loadMovies
from links import loadLinks
from ratings import loadRatings
from tags import loadTags

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/movies")
def get_movies():
    movies = loadMovies("data_base/movies.csv")
    return movies

@app.get("/links")
def get_links():
    links = loadLinks("data_base/links.csv")
    return links

@app.get("/ratings")
def get_ratings():
    ratings = loadRatings("data_base/ratings.csv")
    return ratings

@app.get("/tags")
def get_tags():
    tags = loadTags("data_base/tags.csv")
    return tags
