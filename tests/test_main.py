## tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_users_health():
    response = client.get("/api/users/")
    assert response.status_code == 200

def test_post_api_check():
    payload = {"name": "Test User", "email": "testuser@example.com"}
    response = client.post("/api/users/post_test/", json=payload)
    assert response.status_code == 200

def test_database_insert():
    payload = {"name": "DB User", "email": "dbuser@example.com"}
    response = client.post("/api/users/database_insert_post/", json=payload)
    assert response.status_code == 200

def test_database_get():
    response = client.get(
        "/api/users/database_row_get/",
        params={"name": "DB User", "email": "dbuser@example.com"}
    )
    assert response.status_code == 200

def test_cache_get():
    response = client.get(
        "/api/users/cache_row_get/",
        params={"name": "DB User", "email": "dbuser@example.com"}
    )
    assert response.status_code == 200

    response = client.get(
        "/users/cache_row_get/",
        params={
            "name": "DB User",
            "email": "dbuser@example.com"
        }
    )
    assert response.status_code == 200
    assert "SUCCESS" in response.json()["message"]