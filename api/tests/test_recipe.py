import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_create_recipe():
    response = client.post(
        "/recipe",
        json={
            "title": "Test Recipe",
            "description": "This is a test recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "steps": ["step1", "step2"],
            "time": 30,
            "difficulty": 1,
            "servings": 4
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Recipe",
        "description": "This is a test recipe",
        "ingredients": ["ingredient1", "ingredient2"],
        "steps": ["step1", "step2"],
        "time": 30,
        "difficulty": 1,
        "servings": 4
    }
