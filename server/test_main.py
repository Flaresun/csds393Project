# conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app
from asgi_lifespan import LifespanManager

@pytest_asyncio.fixture
async def async_client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.mark.asyncio
async def test_sign_up_success(async_client):
    response = await async_client.post("/sign_up", json={
        "email": "newuser@example.com",
        "password": "password123",
        "role": "student"
    })
    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_sign_up_missing_fields(async_client):
    response = await async_client.post("/sign_up", json={
        "email": "newuser@example.com",
        "password": ""
    })
    assert response.status_code == 400
