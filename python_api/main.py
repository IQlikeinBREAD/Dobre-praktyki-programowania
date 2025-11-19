from fastapi import FastAPI, Depends, HTTPException
from python_api.sql.DBSQLite import SessionLocal
from sqlalchemy.orm import Session
from python_api.sql.models import Movie, Link, Rating, Tag, User
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
from python_api.auth.authUtils import createToken, verifyToken, SECRET_KEY, ALGORITHM

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
    password = data.password.encode('utf-8')
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    hashed_pw = db.query(User).filter(User.username == username).first().hashed_password.encode('utf-8')
    if not bcrypt.checkpw(password, hashed_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

class CreateUserData(BaseModel):
    username: str
    password: str
    roles: str

@app.post("/users")
def createUser(data: CreateUserData, db: Session = Depends(getDB), user_data: dict=Depends(verifyToken)):
    if user_data.get("roles") != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    username = data.username
    password = data.password.encode('utf-8')
    roles = data.roles
    exsistingUser = db.query(User).filter(User.username == username).first()
    if exsistingUser:
        raise HTTPException(status_code=400, detail="User already exists")
    hashedPw = bcrypt.hashpw(password, bcrypt.gensalt())
    newUser = User(username=username, hashed_password=hashedPw.decode('utf-8'), roles=roles)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    token = createToken(username = newUser.username, roles=newUser.roles)

    return {"msg":"User succesfully created","access_token": token, "token_type": "bearer"}

@app.get("/user_details")
def getUserDetails(user_data: dict=Depends(verifyToken)):
    return {"username": user_data.get("sub"), "roles": user_data.get("roles")}
    


@app.get("/")
def read_root():
    return {"Hello": "world"}


@app.get("/movies")
def get_movies(db: Session = Depends(getDB), user_data: dict=Depends(verifyToken)):
    movies = db.query(Movie).all()
    return [m.__dict__ for m in movies]


@app.get("/links")
def get_links(db: Session = Depends(getDB), user_data: dict=Depends(verifyToken)):
    links = db.query(Link).all()
    return links


@app.get("/ratings")
def get_ratings(db: Session = Depends(getDB), user_data: dict=Depends(verifyToken)):
    ratings = db.query(Rating).all()
    return ratings


@app.get("/tags")
def get_tags(db: Session = Depends(getDB), user_data: dict=Depends(verifyToken)):
    tags = db.query(Tag).all()
    return tags
