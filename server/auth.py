"""
Methods and variables necessary for user authentication
"""

from datetime import datetime, timedelta, timezone
from http.client import HTTPException

import jwt
from pydantic import BaseModel

from passlib.context import CryptContext

from database import get_user
from model import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expiration_delta: timedelta | None = None):
    """
    Create a JWT token from a data dict
    """
    to_encode = data.copy()
    if expiration_delta:
        expire = datetime.now(timezone.utc) + expiration_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token : str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.PyJWTError:
        raise Exception("Token is invalid")

def verify_access_token(token:str):
    try:
        payload = decode_access_token(token)
        return {"success":True, "user": payload["sub"]}
    except Exception as e:
        raise Exception(str(e))

def verify_password(plain_password, hashed_password):
    """
    Verify that the hash of a plain-text password and verify that it matches a given hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hash a plain-text password
    """
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str) -> bool | User:
    """
    Authenticate a user
    """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


