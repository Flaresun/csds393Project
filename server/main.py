import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from prisma import Prisma
import importlib
import sys
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from methods import hash_password, compare_password, get_user_by_email, get_all_users
# Run with comamand : uvicorn main:app --reload

import json
from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks, UploadFile, File
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

app = FastAPI()

load_dotenv()
db = Prisma(auto_register=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

class SignupUser(BaseModel):
    email : str
    password : str
    role : str

@app.post("/signup")
async def signup(user :SignupUser ):
    params = list(user)

    email, password, role = params[0][1], params[1][1], params[2][1]
    if email == "" or password == "" :
        return JSONResponse(content={"success":False, "message":"Email Password and Role Required"},status_code=200,headers={"X-Error": "Custom Error"})
    # Prisma 
    try:
        prisma = Prisma()
        await prisma.connect()
        # Check if email already exists 
        email_check = await get_user_by_email(db,email)
        print(email_check)
        if email_check:
            return JSONResponse(content={"success":False, "message":"User Already Exists"},status_code=200,headers={"X-Error": "Custom Error"})
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
        return JSONResponse(content={"success":False, "message":e},status_code=200,headers={"X-Error": "Custom Error"})

    return JSONResponse(content={"success":True, "message":"Signup Successful", "user":{"email":email}},status_code=201,headers={"X-Error": "Custom Error"})

class LoginUser(BaseModel):
    email : str
    password : str

@app.post("/login")
async def login(user : LoginUser):
    params : list[LoginUser] = list(user)
    email, password = params[0][1], params[1][1]
    if email == "" or password == "" :
        return JSONResponse(content={"success":False, "message":"Email Password and Role Required"},status_code=200,headers={"X-Error": "Custom Error"})
    try:
        await db.disconnect()
        await db.connect()
        user = await get_user_by_email(db,email)

        if not user:
            return JSONResponse(content={"success":False, "message":"User Not Found"},status_code=200,headers={"X-Error": "Custom Error"})

        if not compare_password(password.encode("utf-8"), user['password'].encode("utf-8")):
            return JSONResponse(content={"success":False, "message":"Password is Incorrect"},status_code=200,headers={"X-Error": "Custom Error"})

        return JSONResponse(content={"success":True, "message":"Login Successful", "user":{"email":email}},status_code=200,headers={"X-Error": "Custom Error"})
    except BaseException as e:
        return JSONResponse(content={"success":False, "message":str(e)},status_code=200,headers={"X-Error": "Custom Error"})
