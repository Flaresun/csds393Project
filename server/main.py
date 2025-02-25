"""
Main file containing HTTP endpoint definitions
"""
from contextlib import asynccontextmanager
from datetime import timedelta
import os
from typing import Annotated

import jwt

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from psycopg_pool import AsyncConnectionPool
from pydantic import BaseModel
from prisma import Prisma

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, authenticate_user, create_access_token, \
    get_user, SECRET_KEY
from database import fake_users_db
from model import Token, TokenData, User

from methods import hash_password, compare_password, get_user_by_email, get_all_users
# Run with comamand : uvicorn main:app --reload

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Set up asynchronous connection pool
    """
    app.db_conn_pool = AsyncConnectionPool(os.getenv("DATABASE_URL"))
    yield
    await app.db_conn_pool.close()

app = FastAPI(lifespan=lifespan)
db = Prisma(auto_register=True)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Attempt to get an access token given a username and password
    """
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Attempt to get data about yourself (requires authentication)
    """
    return current_user

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

class SignupUser(BaseModel):
    email: str
    password: str
    role: str

@app.post("/signup")
async def signup(user: SignupUser):
    params = list(user)

    email, password, role = params[0][1], params[1][1], params[2][1]
    if email == "" or password == "":
        return JSONResponse(content={"success": False, "message": "Email Password and Role Required"}, status_code=200, headers={"X-Error": "Custom Error"})
    # Prisma
    try:
        prisma = Prisma()
        await prisma.connect()
        # Check if email already exists
        email_check = await get_user_by_email(db, email)
        print(email_check)
        if email_check:
            return JSONResponse(content={"success": False, "message": "User Already Exists"}, status_code=200, headers={"X-Error": "Custom Error"})
        user = await prisma.user.create(
            data={
                'email': email,
                "password": hash_password(password),
                "role": role
            },
        )

        await prisma.disconnect()
    except BaseException as e:
        await prisma.disconnect()
        return JSONResponse(content={"success": False, "message": e}, status_code=200, headers={"X-Error": "Custom Error"})

    return JSONResponse(content={"success": True, "message": "Signup Successful", "user": {"email": email}}, status_code=201, headers={"X-Error": "Custom Error"})

class LoginUser(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(user: LoginUser):
    params: list[LoginUser] = list(user)
    email, password = params[0][1], params[1][1]
    if email == "" or password == "":
        return JSONResponse(content={"success": False, "message": "Email Password and Role Required"}, status_code=200, headers={"X-Error": "Custom Error"})
    try:
        await db.disconnect()
        await db.connect()
        user = await get_user_by_email(db, email)

        if not user:
            return JSONResponse(content={"success": False, "message": "User Not Found"}, status_code=200, headers={"X-Error": "Custom Error"})

        if not compare_password(password.encode("utf-8"), user['password'].encode("utf-8")):
            return JSONResponse(content={"success": False, "message": "Password is Incorrect"}, status_code=200, headers={"X-Error": "Custom Error"})

        return JSONResponse(content={"success": True, "message": "Login Successful", "user": {"email": email}}, status_code=200, headers={"X-Error": "Custom Error"})
    except BaseException as e:
        return JSONResponse(content={"success": False, "message": str(e)}, status_code=200, headers={"X-Error": "Custom Error"})
