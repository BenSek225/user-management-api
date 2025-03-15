# flask_version/tests/test_routes.py
import pytest
import sys
import os

# Ajoute le dossier parent au chemin pour que Python trouve app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register(client):
    """Teste l’inscription d’un utilisateur."""
    response = client.post("/register", json={"username": "test", "email": "test@example.com", "password": "pass123"})
    assert response.status_code == 201
    assert response.json["username"] == "test"

def test_login(client):
    """Teste la connexion d’un utilisateur."""
    client.post("/register", json={"username": "test", "email": "test@example.com", "password": "pass123"})
    response = client.post("/login", json={"username": "test", "password": "pass123"})
    assert response.status_code == 200
    assert "access_token" in response.json