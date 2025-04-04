"""
Methods and variables necessary for user authentication
"""

from datetime import datetime, timedelta, timezone

import jwt

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from database import get_user
from model import User, Token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

async def authenticate_user(db_conn_pool, email: str, password: str) -> bool | User:
    """
    Authenticate a user
    """
    user = await get_user(db_conn_pool, email)
    if not user:
        return False
    try:
        if not verify_password(password, user.password_hash):
            return False
    except UnknownHashError:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT token from a data dict
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token_from_email(email: str) -> Token:
    """
    A wrapper around create_access_token for JWT creation given just a email string
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
