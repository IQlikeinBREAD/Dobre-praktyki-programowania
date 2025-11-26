from fastapi.testclient import TestClient
from python_api.main import app
from python_api.sql.DBSQLite import SessionLocal
from python_api.sql.models import User
import bcrypt

client = TestClient(app)

def setupModule(module):
    db = SessionLocal()
    hashedPw = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
    adminUser = User(username="admin", hashed_password=hashedPw.decode('utf-8'), roles="ADMIN")
    db.add(adminUser)
    db.commit()
    db.close()

def testLoginSuccess():
    response = client.post("/login", json={
        "username": "admin", 
        "password": "admin"
        })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def testLoginFailure():
    response = client.post("/login", json={"username": "admin", "password": "55"})
    assert response.status_code == 401

def testCreateUserAdmin():
    loginResponse = client.post("/login", json={"username": "admin", "password": "adminpass"})
    token = loginResponse.json()["access_token"]
    response = client.post("/users",headers={"Authorization": f"Bearer {token}"}, 
                                    json={"username": "newuser", "password": "newpass", "roles": "USER"})
    assert response.status_code == 200
    assert response.json()["msg"] == "User succesfully created"

def testCreateUserNonAdmin():
    logindResponse = client.post("/login", json={"username": "admin", "password": "adminpass"})
    token = logindResponse.json()["access_token"]
    response = client.post("/users",headers={"Authorization": f"Bearer {token}"}, 
                                    json={"username": "anotheruser", "password": "anotherpass", "roles": "USER"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"