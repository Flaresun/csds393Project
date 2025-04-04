import pytest
import auth
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import jwt

def test_create_access_token():
    delta = timedelta(minutes=10)
    token = auth.create_access_token({"sub": "testuser"}, expiration_delta=delta)
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    assert payload["sub"] == "testuser"
    assert abs(payload["exp"] - int((datetime.now(timezone.utc) + delta).timestamp())) < 5

def test_decode_access_token():
    token = auth.create_access_token({"sub": "validuser"})
    payload = auth.decode_access_token(token)
    assert payload["sub"] == "validuser"

    # token is expired
    expired_token = jwt.encode(
        {"sub": "expired", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        auth.SECRET_KEY,
        algorithm=auth.ALGORITHM
    )
    with pytest.raises(Exception) as e:
        auth.decode_access_token(expired_token)
    assert "Token expired" in str(e.value)

    # invalid token
    with pytest.raises(Exception) as e:
        auth.decode_access_token("not_a_real_token")
    assert "Token is invalid" in str(e.value)

def test_verify_access_token():
    token = auth.create_access_token({"sub": "verified_user"})
    result = auth.verify_access_token(token)
    assert result == {"success": True, "user": "verified_user"}

    # invalid token
    with pytest.raises(Exception) as e:
        auth.verify_access_token("not_a_valid_token")
    assert "Token is invalid" in str(e.value)

@patch("main.pwd_context.verify")
def test_verify_password(mock_verify):
    mock_verify.return_value = True
    assert auth.verify_password("plain", "hashed") is True

    mock_verify.return_value = False
    assert auth.verify_password("wrong", "hashed") is False

@patch("main.pwd_context.hash")
def test_get_password_hash(mock_hash):
    mock_hash.return_value = "hashed_password"
    assert auth.get_password_hash("mypassword") == "hashed_password"

@pytest.mark.asyncio
@patch("main.get_user")
@patch("main.verify_password")
def test_authenticate_user(mock_verify_password, mock_get_user):
    user = MagicMock()
    user.hashed_password = "hashed123"
    mock_get_user.return_value = user
    mock_verify_password.return_value = True

    result = auth.authenticate_user("fake_db", "valid_user", "correct_password")
    assert result == user

    # user not found
    mock_get_user.return_value = None
    result = auth.authenticate_user("fake_db", "missing_user", "any_password")
    assert result is False

    # wrong password
    mock_get_user.return_value = user  # restore user
    mock_verify_password.return_value = False
    result = auth.authenticate_user("fake_db", "valid_user", "wrong_password")
    assert result is False