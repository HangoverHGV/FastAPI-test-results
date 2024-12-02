import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from database import Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use an in-memory SQLite database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client_with_db(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield client
    app.dependency_overrides.clear()

def test_create_recipe(client_with_db):
    response = client_with_db.post(
        "/recipe",
        json={
            "title": "Test Recipe",
            "description": "This is a test recipe",
            "ingredients": "ingredient1, ingredient2",
            "steps": "step1 step2",
            "time": 30,
            "difficulty": 1,
            "servings": 4
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Test Recipe",
        "description": "This is a test recipe",
        "ingredients": "ingredient1, ingredient2",
        "steps": "step1 step2",
        "time": 30,
        "difficulty": 1,
        "servings": 4
    }

def test_read_recipe(client_with_db):
    response = client_with_db.get("/recipe/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Recipe",
        "description": "This is a test recipe",
        "ingredients": "ingredient1, ingredient2",
        "steps": "step1 step2",
        "time": 30,
        "difficulty": 1,
        "servings": 4
    }

def test_read_all_recipes(client_with_db):
    response = client_with_db.get("/recipe")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test Recipe",
            "description": "This is a test recipe",
            "ingredients": "ingredient1, ingredient2",
            "steps": "step1 step2",
            "time": 30,
            "difficulty": 1,
            "servings": 4
        }
    ]
