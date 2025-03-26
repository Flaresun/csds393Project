import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from prisma import Prisma
import importlib
import sys
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from methods import hash_password, compare_password, get_user_by_email, get_all_users, get_notes_by_class_name
# Run with comamand : uvicorn main:app --reload
import json
import jwt 
from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks, UploadFile, File,Form,Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from fastapi import Cookie
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, create_access_token, decode_access_token, verify_access_token

import io
from google_drive import upload_file
app = FastAPI()
load_dotenv()
db = Prisma(auto_register=True)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        print("not cachje")
        prisma = Prisma()
        await prisma.connect()
        # Check if email already exists 
        email_check = await get_user_by_email(db,email)
        print(email_check)
        if email_check:
            return JSONResponse(content={"success":False, "message":"User Already Exists"},status_code=200,headers={"X-Error": "Custom Error"})
        

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": email}, expiration_delta=access_token_expires)

        res = JSONResponse(content={"success":True, "message":"Signup Successful", "user":{"email":email}},status_code=201,headers={"X-Error": "Custom Error"})
        res.set_cookie(
            key="access_token", value=access_token, httponly=False, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,secure=False
        )

        user = await prisma.user.create(
                data={
                    'email': email,
                    "password": hash_password(password),
                    "role": role                
                },
            )
        await prisma.disconnect()
        return res
    except BaseException as e:
        await prisma.disconnect()
        print("issue")
        return JSONResponse(content={"success":False, "message":e},status_code=200,headers={"X-Error": "Custom Error"})
    
    
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
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": email}, expiration_delta=access_token_expires)

        res = JSONResponse(content={"success":True, "message":"Login Successful", "user":{"email":email}},status_code=200,headers={"X-Error": "Custom Error"})
        res.set_cookie(
            key="access_token", value=access_token, httponly=False, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, path="/", secure=False
        )
        return res
    except BaseException as e:
        return JSONResponse(content={"success":False, "message":str(e)},status_code=200,headers={"X-Error": "Custom Error"})

@app.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    return response


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...),className: str = Form(...),email: str = Form(...)):
    print("Received file:", file.filename)
    print(className)
    print(email)
    await validate_user(request)
    try:
        res : str = await upload_file(db,email,className,file)
        

        return JSONResponse(content={"success":True, "message":res},status_code=200,headers={"X-Error": "Custom Error"})
    except BaseException as e:
        return JSONResponse(content={"success":False, "message":str(e)},status_code=200,headers={"X-Error": "Custom Error"})

class ClassNameModel(BaseModel):
    class_name : str
@app.post("/get_class")
async def get_class(request: Request, class_name : ClassNameModel):
    await validate_user(request)
    try:
        #verify_access_token(token[7:])
        params : list[ClassNameModel] = list(class_name)
        class_name = params[0][1]
        res = await get_notes_by_class_name(db,class_name)
        return JSONResponse(content={"success":True, "message":list(res)},status_code=200,headers={"X-Error": "Custom Error"})
    except BaseException as e:
        return JSONResponse(content={"success":False, "message":str(e)},status_code=200,headers={"X-Error": "Custom Error"}) 

@app.post("/validate_user")
async def validate_user(request: Request):
    token = request.headers.get("Authorization")
    try:
        verify_access_token(token[7:])
        logout()
        return JSONResponse(content={"success":True, "message":"User is Authenticated"},status_code=200,headers={"X-Error": "Custom Error"}) 
    except BaseException as e:
        return JSONResponse(content={"success":False, "message":str(e)},status_code=200,headers={"X-Error": "Custom Error"}) 