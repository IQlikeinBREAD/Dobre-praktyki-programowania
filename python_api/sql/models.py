from sqlalchemy import Column, Integer, Float, String
from python_api.sql.DBSQLite import Base
from sqlalchemy.orm import relationship


class Movie(Base):
    __tablename__ = "movies"
    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genres = Column(String)


class Link(Base):
    __tablename__ = "links"
    movieId = Column(Integer, primary_key=True, index=True)
    imdbId = Column(Integer)
    tmdbId = Column(Integer)


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    movieId = Column(Integer)
    rating = Column(Float)
    timestamp = Column(Integer)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    movieId = Column(Integer)
    tag = Column(String)
    timestamp = Column(Integer)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    roles = Column(String)
