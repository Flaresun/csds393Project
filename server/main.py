import os
from dotenv import load_dotenv

# Run with comamand : uvicorn main:app --reload
from fastapi import FastAPI

app = FastAPI()

load_dotenv()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}
