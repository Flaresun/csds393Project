"""
Main file containing HTTP endpoint definitions
"""
from contextlib import asynccontextmanager
import os
from typing import Annotated

import jwt

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from psycopg_pool import AsyncConnectionPool
from prisma import Prisma

from auth import ALGORITHM, authenticate_user, create_access_token_from_email, \
    get_user, get_password_hash, SECRET_KEY
from database import create_new_user, UserAlreadyExistsException
from model import SignUpRequestData, Token, TokenData, User

# Run with comamand : uvicorn main:app --reload

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db_conn_pool = AsyncConnectionPool(os.getenv("DATABASE_URL"), open=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Set up asynchronous connection pool
    """
    await db_conn_pool.open()
    yield
    await db_conn_pool.close()

app = FastAPI(lifespan=lifespan)
db = Prisma(auto_register=True)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Obtain data about the current user, based on the JWT token in the request header
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    user = await get_user(db_conn_pool, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Attempts to get an access token given a username and password
    """
    user = await authenticate_user(
        db_conn_pool, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token_from_email(user.email)

@app.post("/sign_up")
async def sign_up(request_data: SignUpRequestData) -> Token:
    """
    Attempts to create a new user in the database, and then return an access token for that user
    """
    email = request_data.email
    password = request_data.password
    role = request_data.role
    param_list = [email, password, role]
    if None in param_list or "" in param_list:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="email, password and role are required"
        )
    if role not in ["student", "faculty"]:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="role must be student or faculty"
        )
    password_hash = get_password_hash(password)
    try:
        await create_new_user(db_conn_pool, email, password_hash, role)
    except UserAlreadyExistsException as exc:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="email already in use"
        ) from exc
    return create_access_token_from_email(email)

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Attempt to get data about yourself (requires authentication)
    """
    return current_user
