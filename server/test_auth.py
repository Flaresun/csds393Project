from datetime import timedelta
from unittest.mock import AsyncMock, patch

import jwt
import pytest

from auth import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    create_access_token_from_email,
    SECRET_KEY,
    ALGORITHM
)
from model import Token, UserInDB


def test_verify_password_and_hash():
    plain_password = "securepassword123"
    hashed = get_password_hash(plain_password)
    assert verify_password(plain_password, hashed)
    assert not verify_password("wrongpassword", hashed)


@pytest.mark.asyncio
async def test_authenticate_user():
    # no user found
    with patch("auth.get_user", new=AsyncMock(return_value=None)):
        result = await authenticate_user(None, "nonexistent@example.com", "1234")
        assert result is False

    fake_user = UserInDB(
        id=1,
        email="test@example.com",
        role="student",
        password_hash=get_password_hash("1234")
    )

    # success
    with patch("auth.get_user", new=AsyncMock(return_value=fake_user)):
        result = await authenticate_user(None, "test@example.com", "1234")
        assert isinstance(result, UserInDB)
        assert result.email == "test@example.com"
        assert result.role == "student"

    # wrong password
    with patch("auth.get_user", new=AsyncMock(return_value=fake_user)):
        result = await authenticate_user(None, "test@example.com", "wrong")
        assert result is False


def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, timedelta(minutes=5))
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded


def test_create_access_token_from_email():
    email = "test@example.com"
    token_obj = create_access_token_from_email(email)
    assert isinstance(token_obj, Token)
    decoded = jwt.decode(token_obj.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == email
    assert "exp" in decoded
