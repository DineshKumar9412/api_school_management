## tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, Base
from app.database.session import get_db

# Correct MySQL URL (with the proper username, password, and encoding)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root%40123@localhost:3306/testdb"

# Create the SQLAlchemy engine with the MySQL connection string
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session maker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all the tables in the database (if not already created)
Base.metadata.create_all(bind=engine)

# TestClient for FastAPI testing
client = TestClient(app)



def test_read_root():
    # Test the GET request at the root
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    # Test the POST request to create an item
    item_data = {"name": "Sample Item", "description": "This is a test item"}
    response = client.post("/items/", json=item_data)
    
    assert response.status_code == 200
    assert response.json() == item_data

def test_create_item_no_description():
    # Test the POST request to create an item without description
    item_data = {"name": "Sample Item Without Description"}
    response = client.post("/items/", json=item_data)
    
    assert response.status_code == 200
    assert response.json() == {"name": "Sample Item Without Description", "description": None}

def test_get_value():
    # Test the new GET request at /get_value/
    query_params = {"name": "Sample Name", "description": "Sample Description"}
    
    # Sending the GET request with query parameters
    response = client.get("/get_value/", params=query_params)
    
    assert response.status_code == 200
    assert response.json() == {
        "name": "Sample NameUSER_TEST",
        "description": "Sample DescriptionUSER_TEST"
    }

def test_create_item_value():
    item_data = {
        "id": 1,
        "name": "dinesh",
        "description": "This is a test item",
        "price": 99.99
    }
    response = client.post("/create_item/", json=item_data)

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "dinesh",
        "description": "This is a test item",
        "price": 99.99
    }


def test_create_user():
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    
    # Sending the POST request to create a user
    response = client.post("/post_users_db/", json=user_data)
    
    assert response.status_code == 200
    
    # Assert that the response contains the correct user data
    response_data = response.json()
    assert response_data["name"] == "John Doe"
    assert response_data["email"] == "john.doe@example.com"
    
    # Assert that the id is present and is a positive integer
    assert "id" in response_data
    assert isinstance(response_data["id"], int)
    assert response_data["id"] > 0

# Test GET /get_users_db/{user_id} endpoint
def test_get_user():
    user_data = {"name": "Jane Doe", "email": "jane.doe@example.com"}
    response = client.post("/post_users_db/", json=user_data)
    user_id = response.json()['id']  # Get the id of the created user
    
    response = client.get(f"/get_users_db/{user_id}")
    
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "name": "Jane Doe", "email": "jane.doe@example.com"}

def test_get_user_not_found():
    response = client.get("/get_users_db/999")  # Using an arbitrary non-existent user_id
    
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}