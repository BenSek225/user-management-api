# fastapi_version/tests/test_routes.py
import pytest
import pytest_asyncio
import sys
import os
from httpx import AsyncClient, ASGITransport  # Ajoute ASGITransport

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from database import Base, engine, get_db
from sqlalchemy.orm import Session

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        Base.metadata.create_all(bind=engine)
        yield ac
        Base.metadata.drop_all(bind=engine)

@pytest_asyncio.fixture
async def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/register", json={
        "username": "test",
        "email": "test@example.com",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "test"

@pytest.mark.asyncio
async def test_login(client):
    await client.post("/register", json={
        "username": "test",
        "email": "test@example.com",
        "password": "pass123"
    })
    response = await client.post("/login", json={
        "username": "test",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()