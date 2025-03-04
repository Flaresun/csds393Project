from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks, UploadFile, File
from methods import hash_password, compare_password, get_user_by_email, get_all_users
import io
import json
from prisma import Prisma
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import jwt

from server.auth import ALGORITHM, SECRET_KEY
from server.database import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()

load_dotenv()
db = Prisma(auto_register=True)

# service account credentials
SERVICE_ACCOUNT_FILE = "service_account_credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# authenticate using service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=credentials)


async def upload_to_drive(file: UploadFile):
    file_metadata = {"name": file.filename}
    media = MediaIoBaseUpload(io.BytesIO(await file.read()), mimetype="application/pdf")

    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    file_url = f"https://drive.google.com/file/d/{uploaded_file['id']}/view"

    return file_url

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user  # authenticated user object

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in ["Student"]:
        raise HTTPException(status_code=403, detail="Permission denied.")

    # upload file to Google Drive
    file_metadata = {"name": file.filename}
    media = MediaIoBaseUpload(io.BytesIO(await file.read()), mimetype="application/pdf")
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    file_id = uploaded_file["id"]
    file_url = f"https://drive.google.com/file/d/{file_id}/view"

    # stores metadata in Neon
    await db.connect()
    await db.fileupload.create(data={
        "file_id": file_id,
        "file_url": file_url,
        "uploaded_by": current_user["id"]
    })
    await db.disconnect()

    return {"message": "File uploaded successfully!", "file_url": file_url}
