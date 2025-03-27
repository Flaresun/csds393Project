"""
Main file containing HTTP endpoint definitions
"""
from contextlib import asynccontextmanager
import os
from typing import Annotated

import jwt

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from psycopg_pool import AsyncConnectionPool
from prisma import Prisma

from auth import ALGORITHM, authenticate_user, create_access_token_from_email, \
    get_user, get_password_hash, SECRET_KEY
from database import CourseAlreadyExistsException, CourseDoesNotExistException, create_new_course, \
    create_new_section, create_new_user, delete_note as delete_note_from_db, \
        DepartmentDoesNotExistException, FacultyDoesNotExistException, get_courses_for_department,\
            get_department_codes, get_note as get_note_from_db, get_notes_for_course as \
                get_notes_for_course_from_db, get_notes_for_section as \
                    get_notes_for_section_from_db, get_notes_for_user, get_section_ids_for_course,\
                        InvalidSemesterException, NoteDoesNotExistException, \
                            SectionAlreadyExistsException, SectionDoesNotExistException, \
                                set_or_update_note_rating, store_note, UserAlreadyExistsException,\
                                    UserIsNotOwnerOrFacultyException
from model import CreateCourseRequestData, CreateSectionRequestData, DeleteNoteRequestData, \
    GetCoursesRequestData, GetMyNotesRequestData, GetNoteRequestData, \
        GetNotesForCourseRequestData, GetNotesForSectionRequestData, GetSectionsRequestData, \
            RateNoteRequestData, SignUpRequestData, Token, TokenData, UploadNoteRequestData, User

# Run with comamand "uvicorn main:app --reload" or "fastapi dev main.py"

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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email, password and role are required"
        )
    if role not in ["student", "faculty"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="role must be student or faculty"
        )
    password_hash = get_password_hash(password)
    try:
        await create_new_user(db_conn_pool, email, password_hash, role)
    except UserAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already in use"
        ) from exc
    return create_access_token_from_email(email)

@app.post("/create_course")
async def create_course(
    current_user: Annotated[User, Depends(get_current_user)], request_data: CreateCourseRequestData
):
    """
    Attempts to create a new course in a particular department
    """
    if current_user.role != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only faculty can create course"
        )
    try:
        await create_new_course(
            db_conn_pool, request_data.department, request_data.code, request_data.name
        )
    except DepartmentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department does not exist"
        ) from exc
    except CourseAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course already exists"
        ) from exc
    return Response(content=None)

@app.post("/create_section")
async def create_section(
    current_user: Annotated[User, Depends(get_current_user)], request_data: CreateSectionRequestData
):
    """
    Attempts to create a new course in a particular department
    """
    if current_user.role != "faculty":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only faculty can create section"
        )
    try:
        section_id = await create_new_section(
            db_conn_pool,
            request_data.department,
            request_data.course,
            request_data.instructor,
            request_data.year,
            request_data.semester,
        )
    except DepartmentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department does not exist"
        ) from exc
    except CourseDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course does not exist"
        ) from exc
    except FacultyDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="instructor (user with faculty role) does not exist"
        ) from exc
    except InvalidSemesterException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="semester must be one of 'fall', 'spring', 'summer'"
        ) from exc
    except SectionAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course already exists"
        ) from exc
    return JSONResponse(
        content = {
            "id": section_id
        }
    )

@app.post("/get_notes_for_course")
async def get_notes_for_course(request_data: GetNotesForCourseRequestData):
    """
    Attempts to get notes for all sections of a particular course
    """
    try:
        notes = await get_notes_for_course_from_db(
            db_conn_pool, request_data.department, request_data.course, not request_data.ids_only
        )
        serializable_notes = []
        for note in notes:
            serializable_note = {
                "id": note.note_id,
                "section_id": note.section_id,
                "owner_id": note.owner_id
            }
            if note.content is not None:
                serializable_note["content"] = note.content
            serializable_notes.append(serializable_note)
        return JSONResponse(
            content = {
                "notes": serializable_notes
            }
        )
    except DepartmentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department does not exist"
        ) from exc
    except CourseDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course does not exist"
        ) from exc

@app.get("/get_departments")
async def get_departments():
    """
    Attempts to get the codes of all available departments
    """
    departments = await get_department_codes(db_conn_pool)
    return JSONResponse(
        content = {
            "departments": departments
        }
    )

@app.post("/get_courses")
async def get_courses(request_data: GetCoursesRequestData):
    """
    Attempts to get the codes of all courses in a particular department
    """
    try:
        courses = await get_courses_for_department(db_conn_pool, request_data.department)
        return JSONResponse(
            content = {
                "courses": courses
            }
        )
    except DepartmentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department does not exist"
        ) from exc

@app.post("/get_sections")
async def get_sections(request_data: GetSectionsRequestData):
    """
    Attempts to get IDs of all sections of a particular course
    """
    try:
        section_ids = await get_section_ids_for_course(
            db_conn_pool, request_data.department, request_data.course
        )
        return JSONResponse(
            content = {
                "section_ids": section_ids
            }
        )
    except DepartmentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department does not exist"
        ) from exc
    except CourseDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course does not exist"
        ) from exc

@app.post("/upload_note")
async def upload_note(
    current_user: Annotated[User, Depends(get_current_user)], request_data: UploadNoteRequestData
):
    """
    Attempts to upload a note for a particular section
    """
    # We don't catch UserDoesNotExistException because that shouldn't happen: if an account for
    # the caller doesn't exist, authentication should fail.
    try:
        note_id = await store_note(
            db_conn_pool, request_data.section_id, request_data.content, current_user.email
        )
        return JSONResponse(
            content = {
                "id": note_id
            }
        )
    except SectionDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="section does not exist"
        ) from exc

@app.post("/delete_note")
async def delete_note(
    current_user: Annotated[User, Depends(get_current_user)], request_data: DeleteNoteRequestData
):
    """
    Attempts to delete the note with the specified id
    """
    try:
        await delete_note_from_db(
            db_conn_pool, request_data.note_id, current_user.email
        )
        return Response(content=None)
    except NoteDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="note does not exist"
        ) from exc
    except UserIsNotOwnerOrFacultyException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only note owner or faculty can delete note"
        ) from exc

@app.post("/get_note")
async def get_note(request_data: GetNoteRequestData):
    """
    Attempts to get the note with the specified id
    """
    try:
        note = await get_note_from_db(
            db_conn_pool, request_data.note_id
        )
        serializable_note = {
            "id": note.note_id,
            "section_id": note.section_id,
            "owner_id": note.owner_id,
            "content": note.content,
        }
        return JSONResponse(
            content = serializable_note
        )
    except NoteDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="note does not exist"
        ) from exc

@app.post("/get_notes_for_section")
async def get_notes_for_section(request_data: GetNotesForSectionRequestData):
    """
    Attempts to get notes for a particular section of a course.
    """
    try:
        notes = await get_notes_for_section_from_db(
            db_conn_pool, request_data.section_id, not request_data.ids_only
        )
        serializable_notes = []
        for note in notes:
            serializable_note = {
                "id": note.note_id,
                "section_id": note.section_id,
                "owner_id": note.owner_id
            }
            if note.content is not None:
                serializable_note["content"] = note.content
            serializable_notes.append(serializable_note)
        return JSONResponse(
            content = {
                "notes": serializable_notes
            }
        )
    except SectionDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="section does not exist"
        ) from exc

@app.post("/get_my_notes")
async def get_my_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    request_data: GetMyNotesRequestData
):
    """
    Attempts to get all the user's notes
    """
    notes = await get_notes_for_user(
        db_conn_pool, current_user.email, not request_data.ids_only
    )
    serializable_notes = []
    for note in notes:
        serializable_note = {
            "id": note.note_id,
            "section_id": note.section_id,
            "owner_id": note.owner_id
        }
        if note.content is not None:
            serializable_note["content"] = note.content
        serializable_notes.append(serializable_note)
    return JSONResponse(
        content = {
            "notes": serializable_notes
        }
    )

@app.post("/rate_note")
async def rate_note(
    current_user: Annotated[User, Depends(get_current_user)],
    request_data: RateNoteRequestData
):
    """
    Attempts to leave a rating from a particular user on a particular note
    """
    try:
        rating = request_data.rating
        if rating < 1 or rating > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="rating must be integer between 1 and 10 inclusive"
            )
        await set_or_update_note_rating(
            db_conn_pool, current_user.email, request_data.note_id, request_data.rating
        )
    except NoteDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="note does not exist"
        ) from exc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
