import pytest
from fastapi.testclient import TestClient
from python_api.main import app, getDB
from python_api.sql.DBSQLite import Base, engine, SessionLocal
from python_api.sql.models import User, Movie
import bcrypt
from python_api.auth.authUtils import createToken

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    hashed_pw = bcrypt.hashpw(b"adminpass", bcrypt.gensalt()).decode("utf-8")
    admin = User(username="admin", hashed_password=hashed_pw, roles="ADMIN")
    db.add(admin)

    movie = Movie(movieId=123, title="Pony", genres="Fantasy")
    db.add(movie)

    db.commit()
    db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_headers():
    token = createToken(username="admin", roles="ADMIN")
    return {"Authorization": f"Bearer {token}"}
