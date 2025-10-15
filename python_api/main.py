from typing import Union
from fastapi import FastAPI
from movie import Movie, load_movies

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "world"}

@app.get("/movies")
def get_movies():
    movies = load_movies("data_base/movies.csv")
    return [movie.__dict__ for movie in movies]