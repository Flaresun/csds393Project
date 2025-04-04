from __main__ import app, db_conn_pool
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient

import pytest
from fastapi.testclient import TestClient
from jwt import InvalidTokenError

client = TestClient(app)


@pytest.mark.asyncio
@patch.object(db_conn_pool, 'open', new_callable=AsyncMock)
@patch.object(db_conn_pool, 'close', new_callable=AsyncMock)
async def test_lifespan(mock_close, mock_open):
    # simulates application startup
    async with app.router.lifespan_context(app) as lifespan:
        assert mock_open.called
        assert not mock_close.called
    # simulates application shutdown
    assert mock_close.called

@pytest.mark.asyncio
@patch("main.get_user_by_email", new_callable=AsyncMock)
@patch("main.hash_password")
@patch("main.create_access_token")
@patch("main.Prisma")
async def test_signup(mock_prisma, mock_create_token, mock_hash_password, mock_get_user_by_email):
    client = AsyncClient(app=app, base_url="http://test")

    mock_get_user_by_email.return_value = None
    mock_create_token.return_value = "mocked_token"
    mock_hash_password.return_value = "hashed_pw"
    mock_prisma.return_value.user.create = AsyncMock()
    mock_prisma.return_value.connect = AsyncMock()
    mock_prisma.return_value.disconnect = AsyncMock()

    response = await client.post("/signup", json={"email": "new@example.com", "password": "password", "role": "student"})
    assert response.status_code == 201
    assert response.json()["success"] is True

    # missing email
    response = await client.post("/signup", json={"email": "", "password": "password", "role": "student"})
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "Email Password and Role Required"}

    # user already exists
    mock_get_user_by_email.return_value = {"email": "existing@example.com"}
    response = await client.post("/signup", json={"email": "existing@example.com", "password": "password", "role": "student"})
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "User Already Exists"}

    await client.aclose()

@pytest.mark.asyncio
@patch("main.get_user_by_email", new_callable=AsyncMock)
@patch("main.compare_password")
async def test_login(mock_compare_password, mock_get_user_by_email):
    client = AsyncClient(app=app, base_url="http://test")

    mock_get_user_by_email.return_value = {"email": "user@example.com", "password": "hashed_pw"}
    mock_compare_password.return_value = True

    response = await client.post("/login", json={"email": "user@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["success"] is True

    # missing email
    response = await client.post("/login", json={"email": "", "password": "password"})
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "Email Password and Role Required"}

    # user not found
    mock_get_user_by_email.return_value = None
    response = await client.post("/login", json={"email": "nouser@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "User Not Found"}

    # incorrect password
    mock_get_user_by_email.return_value = {"email": "user@example.com", "password": "hashed_pw"}
    mock_compare_password.return_value = False
    response = await client.post("/login", json={"email": "user@example.com", "password": "wrong"})
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "Password is Incorrect"}

    await client.aclose()

@pytest.mark.asyncio
async def test_logout():
    client = AsyncClient(app=app, base_url="http://test")
    response = await client.post("/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out"}
    await client.aclose()

@pytest.mark.asyncio
@patch("main.upload_file", new_callable=AsyncMock)
@patch("main.validate_user", new_callable=AsyncMock)
async def test_upload(mock_validate_user, mock_upload_file):
    client = AsyncClient(app=app, base_url="http://test")

    mock_validate_user.return_value = None
    mock_upload_file.return_value = "Upload successful"

    files = {"file": ("test.txt", b"file content", "text/plain")}
    data = {"email": "user@example.com", "className": "CS101"}
    response = await client.post("/upload", files=files, data=data)
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Upload successful"}

    # simulate upload failure
    mock_upload_file.side_effect = Exception("Failed to upload file")
    response = await client.post("/upload", files=files, data=data)
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "Failed to upload file"}

    await client.aclose()

@patch("main.validate_user", new_callable=AsyncMock)
@patch("main.get_notes_by_class_name", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_get_class(mock_get_notes_by_class_name, mock_validate_user):
    client = AsyncClient(app=app, base_url="http://test")

    mock_validate_user.return_value = None
    mock_get_notes_by_class_name.return_value = [{"note": "Test note"}]

    # valid case
    response = await client.post("/get_class", json={"class_name": "CS101"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": [{"note": "Test note"}]}

    # simulates exception
    mock_get_notes_by_class_name.side_effect = Exception("Class Not Found")
    response = await client.post("/get_class", json={"class_name": "INVALID"})
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "Class Not Found"}

    await client.aclose()

@pytest.mark.asyncio
@patch("main.logout")
@patch("main.verify_access_token")
async def test_validate_user(mock_verify_access_token, mock_logout):
    client = AsyncClient(app=app, base_url="http://test")

    headers = {"Authorization": "Bearer valid_token"}
    mock_verify_access_token.return_value = None
    mock_logout.return_value = None

    response = await client.post("/validate_user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "User is Authenticated"}

    # invalid token
    mock_verify_access_token.side_effect = Exception("Invalid token")
    response = await client.post("/validate_user", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"success": False, "message": "Invalid token"}

    await client.aclose()
