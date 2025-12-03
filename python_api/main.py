import json
from fastapi import FastAPI, Depends, HTTPException
from python_api.sql.DBSQLite import SessionLocal
from sqlalchemy.orm import Session
from python_api.sql.models import Movie, Link, Rating, Tag, User
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
from python_api.auth.authUtils import createToken, verifyToken, SECRET_KEY, ALGORITHM
import numpy as np
import cv2
import requests
import pika

app = FastAPI()


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginData(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(data: LoginData, db: Session = Depends(getDB)):
    username = data.username
    password = data.password.encode("utf-8")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    hashed_pw = (
        db.query(User)
        .filter(User.username == username)
        .first()
        .hashed_password.encode("utf-8")
    )
    if not bcrypt.checkpw(password, hashed_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "roles": user.roles,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


class CreateUserData(BaseModel):
    username: str
    password: str
    roles: str


@app.post("/users")
def createUser(
    data: CreateUserData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    username = data.username
    password = data.password.encode("utf-8")
    roles = data.roles
    exsistingUser = db.query(User).filter(User.username == username).first()
    if exsistingUser:
        raise HTTPException(status_code=400, detail="User already exists")
    hashedPw = bcrypt.hashpw(password, bcrypt.gensalt())
    newUser = User(
        username=username, hashed_password=hashedPw.decode("utf-8"), roles=roles
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    token = createToken(username=newUser.username, roles=newUser.roles)

    return {
        "msg": "User succesfully created",
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/users")
def getUsers(db: Session = Depends(getDB)):

    users = db.query(User).all()
    return [
        {"username": u.username, "password": u.hashed_password, "roles": u.roles}
        for u in users
    ]


@app.get("/user_details")
def getUserDetails(user_data: dict = Depends(verifyToken)):
    return {"username": user_data.get("sub"), "roles": user_data.get("roles")}


@app.get("/")
def read_root():
    return {"Hello": "world"}


class CreateMovieData(BaseModel):
    title: str
    genres: str


@app.post("/movies")
def create_movie(
    data: CreateMovieData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    tittle = data.title
    genres = data.genres
    existingMovie = db.query(Movie).filter(Movie.title == tittle).first()
    if existingMovie:
        raise HTTPException(status_code=400, detail="Movie already exists")
    newMovie = Movie(title=tittle, genres=genres)
    db.add(newMovie)
    db.commit()
    db.refresh(newMovie)

    return {"msg": "Movie succesfully created", "movieId": newMovie.movieId}


@app.get("/movies")
def get_movies(db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)):
    movies = db.query(Movie).all()
    return [m.__dict__ for m in movies]


@app.get("/movies/{movie_id}")
def get_movie(
    movie_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie.__dict__


class UpdateMovieData(BaseModel):
    title: str
    genres: str


@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    data: CreateMovieData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.title = data.title
    movie.genres = data.genres
    db.commit()
    db.refresh(movie)
    return {"msg": "Movie succesfully updated", "movieId": movie.movieId}


@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"msg": "Movie succesfully deleted", "movieId": movie_id}


class CreateLinkData(BaseModel):
    movieId: int
    imbdId: int
    tmdbId: int


@app.get("/links")
def get_links(db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)):
    links = db.query(Link).all()
    return links


@app.get("/links/{movie_id}")
def get_link(
    movie_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@app.post("/links")
def create_link(
    data: CreateLinkData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    movieId = data.movieId
    imbdId = data.imbdId
    tmdbId = data.tmdbId
    existingLink = db.query(Link).filter(Link.movieId == movieId).first()
    if existingLink:
        raise HTTPException(
            status_code=400, detail="Link for this movie already exists"
        )
    newLink = Link(movieId=movieId, imdbId=imbdId, tmdbId=tmdbId)
    db.add(newLink)
    db.commit()
    db.refresh(newLink)
    return {"msg": "Link succesfully created", "movieId": newLink.movieId}


class UpdateLinkData(BaseModel):
    imbdId: int
    tmdbId: int


@app.put("/links/{movie_id}")
def update_link(
    movie_id: int,
    data: UpdateLinkData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    link.imdbId = data.imbdId
    link.tmdbId = data.tmdbId
    db.commit()
    db.refresh(link)
    return {"msg": "Link succesfully updated", "movieId": link.movieId}


@app.delete("/links/{movie_id}")
def delete_link(
    movie_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    link = db.query(Link).filter(Link.movieId == movie_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return {"msg": "Link succesfully deleted", "movieId": movie_id}


class CreateRatingData(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int


@app.get("/ratings")
def get_ratings(db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)):
    ratings = db.query(Rating).all()
    return ratings


@app.get("/ratings/{rating_id}")
def get_rating(
    rating_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@app.post("/ratings")
def create_rating(
    data: CreateRatingData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    userId = data.userId
    movieId = data.movieId
    rating = data.rating
    timestamp = data.timestamp
    newRating = Rating(
        userId=userId, movieId=movieId, rating=rating, timestamp=timestamp
    )
    db.add(newRating)
    db.commit()
    db.refresh(newRating)
    return {"msg": "Rating succesfully created", "id": newRating.id}


class UpdateRatingData(BaseModel):
    rating: float
    timestamp: int


@app.put("/ratings/{rating_id}")
def update_rating(
    rating_id: int,
    data: UpdateRatingData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    rating.rating = data.rating
    rating.timestamp = data.timestamp
    db.commit()
    db.refresh(rating)
    return {"msg": "Rating succesfully updated", "id": rating.id}


@app.delete("/ratings/{rating_id}")
def delete_rating(
    rating_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    db.delete(rating)
    db.commit()
    return {"msg": "Rating succesfully deleted", "id": rating_id}


class CreateTagData(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int


@app.post("/tags")
def create_tag(
    data: CreateTagData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    userId = data.userId
    movieId = data.movieId
    tag = data.tag
    timestamp = data.timestamp
    newTag = Tag(userId=userId, movieId=movieId, tag=tag, timestamp=timestamp)
    db.add(newTag)
    db.commit()
    db.refresh(newTag)
    return {"msg": "Tag succesfully created", "id": newTag.id}


@app.get("/tags")
def get_tags(db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)):
    tags = db.query(Tag).all()
    return tags


@app.get("/tags/{tag_id}")
def get_tag(
    tag_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


class UpdateTagData(BaseModel):
    tag: str
    timestamp: int


@app.put("/tags/{tag_id}")
def update_tag(
    tag_id: int,
    data: UpdateTagData,
    db: Session = Depends(getDB),
    user_data: dict = Depends(verifyToken),
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag.tag = data.tag
    tag.timestamp = data.timestamp
    db.commit()
    db.refresh(tag)
    return {"msg": "Tag succesfully updated", "id": tag.id}


@app.delete("/tags/{tag_id}")
def delete_tag(
    tag_id: int, db: Session = Depends(getDB), user_data: dict = Depends(verifyToken)
):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"msg": "Tag succesfully deleted", "id": tag_id}

class AnalyzeImageData(BaseModel):
    image_url: str

@app.post("/analyze_img")
def analyze_image(data: AnalyzeImageData):

    image_url = data.image_url
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='image_analysis_queue')
    
    message_body = {
        "image_url": image_url,
        "status": "pending"
    }

    channel.basic_publish(
        exchange='',
        routing_key='image_analysis_queue',
        body=json.dumps(message_body)
    )
    
    print(f" [x] Wysłano do kolejki: {image_url}")
    connection.close()

    return {"msg": "Zadanie przyjęte do analizy", "status": "processing_in_background"}