"""
Main file containing HTTP endpoint definitions
"""

from base64 import b64encode
from contextlib import asynccontextmanager
import os
from typing import Annotated

import jwt
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, HTTPException, Response, status, UploadFile, Request, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from psycopg_pool import AsyncConnectionPool

from summary import get_top_keyphrases_from_note_comments

from auth import ALGORITHM, authenticate_user, create_access_token_from_email, \
    get_user, get_password_hash, SECRET_KEY

from database import CourseAlreadyExistsException, CourseDoesNotExistException, create_new_course, \
    create_new_section, create_new_user, delete_note as delete_note_from_db, \
    DepartmentDoesNotExistException, FacultyDoesNotExistException, get_average_note_rating as \
    get_average_note_rating_from_db, get_comments_for_note as get_comments_for_note_from_db, \
    get_courses_for_department, get_department_codes, get_note as get_note_from_db, \
    get_notes_for_course as get_notes_for_course_from_db, get_notes_for_section as \
    get_notes_for_section_from_db, get_notes_for_user, get_role_given_email as \
    get_role_given_email_from_db, get_role_given_user_id as get_role_given_user_id_from_db, \
    get_sections_for_course, InvalidSemesterException, leave_comment_on_note, Note, \
    NoteDoesNotExistException, ParentCommentDoesNotExistException, SectionAlreadyExistsException, \
    SectionDoesNotExistException, set_or_update_note_rating, store_note, \
    UserAlreadyExistsException, UserDoesNotExistException, UserIsNotOwnerOrFacultyException

from model import CreateCourseRequestData, CreateSectionRequestData, DeleteNoteRequestData, \
    GetAverageNoteRatingRequestData, GetCommentsForNoteRequestData, GetCoursesRequestData, \
    GetMyNotesRequestData, GetNoteRequestData, GetNotesForDepartmentAndCourseStringRequestData, \
    GetNotesForCourseRequestData, GetNotesForSectionRequestData, GetRoleGivenEmailRequestData, \
    GetRoleGivenUserIdRequestData, GetSectionsRequestData, LeaveCommentRequestData, \
    RateNoteRequestData, SignUpRequestData, Token, TokenData, User

# Run using: `uvicorn main:app --reload` or `fastapi dev main.py`

# Length of time (in minutes) that access tokens remain valid
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Load environment variables from .env file
load_dotenv()

# Setup OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Asynchronous connection pool to PostgreSQL using psycopg
db_conn_pool = AsyncConnectionPool(os.getenv("DATABASE_URL"), open=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown logic for FastAPI app:
    - Opens database connection pool on startup
    - Closes database connection pool on shutdown
    """
    await db_conn_pool.open()
    yield
    await db_conn_pool.close()

# Create the FastAPI app
app = FastAPI(lifespan=lifespan)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves the current user from the JWT token in the request.

    Args:
        token (str): Bearer token from the Authorization header.

    Returns:
        User object corresponding to the token.
    
    Raises:
        HTTPException: if the token is invalid or the user doesn't exist.
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

@app.post("/validate_user")
async def validate(request: Request):
    """
    Validates whether the current request has a valid authenticated user.

    Returns:
        JSONResponse containing user info if authenticated.
    """
    token = request.headers.get("Authorization")
    data = await get_current_user(token[7:])
    res = JSONResponse(
        content={"success": True, "message": "Login Successful", "user": data.email},
        status_code=200,
        headers={"X-Error": "Custom Error"}
    )
    return res

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Authenticates a user and returns an access token cookie.

    Args:
        form_data: contains username and password.

    Returns:
        JSONResponse with token in cookie and user info.
    """
    user = await authenticate_user(db_conn_pool, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    res = JSONResponse(
        content={"success": True, "message": "Login Successful", "user": {"email": form_data.username}},
        status_code=200,
        headers={"X-Error": "Custom Error"}
    )
    res.set_cookie(
        key="token",
        value=create_access_token_from_email(form_data.username).access_token,
        httponly=False,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        secure=False
    )
    return res

@app.post("/logout")
async def logout():
    """
    Clears the token cookie from the client.
    """
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("token")
    return response

@app.post("/sign_up")
async def sign_up(request_data: SignUpRequestData) -> Token:
    """
    Creates a new user account and returns a token cookie.

    Args:
        request_data: contains email, password, and role (student/faculty)

    Returns:
        JSONResponse with access token and user info.

    Raises:
        HTTPException: if role is invalid or user already exists.
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

    res = JSONResponse(
        content={"success": True, "message": "Login Successful", "user": {"email": email}},
        status_code=200,
        headers={"X-Error": "Custom Error"}
    )
    res.set_cookie(
        key="token",
        value=create_access_token_from_email(email).access_token,
        httponly=False,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        secure=False
    )
    return res

@app.post("/create_course")
async def create_course(
    current_user: Annotated[User, Depends(get_current_user)],
    request_data: CreateCourseRequestData
):
    """
    Creates a new course in a specified department.

    Args:
        current_user: the user making the request.
        request_data: department, course code, and course name.

    Returns:
        JSONResponse confirming course creation.

    Raises:
        HTTPException: if user is not faculty or course/department already exists.
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

    return JSONResponse(
        content={"success": True, "data": {
            "department": request_data.department,
            "code": request_data.code,
            "name": request_data.name
        }, "message": "Course Created Successfully!"},
        status_code=200,
        headers={"X-Error": "Custom Error"}
    )

@app.post("/create_section")
async def create_section(
    current_user: Annotated[User, Depends(get_current_user)],
    request_data: CreateSectionRequestData
):
    """
    Creates a new section for an existing course.

    Args:
        current_user: the user making the request.
        request_data: department, course, instructor, year, and semester.

    Returns:
        JSONResponse confirming section creation.

    Raises:
        HTTPException: for various invalid inputs or authorization failures.
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
        content={"success": True, "data": {
            "department": request_data.department,
            "course": request_data.course,
            "instructor": request_data.instructor,
            "year": request_data.year,
            "semester": request_data.semester
        }, "message": "Section Created Successfully!"},
        status_code=200,
        headers={"X-Error": "Custom Error"}
    )

def create_serializable_note(note: Note) -> dict:
    """
    Creates a serializable dictionary from a Note object as returned by database code.
    If content is present, encodes the content bytes as a Base64 string.

    Args:
        note (Note): The note object to be serialized.

    Returns:
        dict: A dictionary representing the serializable note.
    """
    serializable_note = {
        "id": note.note_id,
        "section_id": note.section_id,
        "owner_id": note.owner_id,
        "content_type": note.content_type
    }
    # If content exists, encode it in Base64 and add it to the dictionary.
    if note.content is not None:
        serializable_note["content"] = b64encode(note.content).decode("ascii")
    return serializable_note

def create_serializable_notes(notes):
    """
    A wrapper function around create_serializable_note that accepts a list of Note objects
    and returns a list of serialized notes.

    Args:
        notes (list): List of Note objects to be serialized.

    Returns:
        list: List of dictionaries representing the serialized notes.
    """
    serializable_notes = []
    for note in notes:
        serializable_note = create_serializable_note(note)
        serializable_notes.append(serializable_note)
    return serializable_notes

async def get_serializable_notes_for_department_and_course_strings(department, course, ids_only):
    """
    Fetches notes for a specific department and course, serializes them, 
    and handles exceptions in a standardized way.

    Args:
        department (str): The department code.
        course (str): The course code.
        ids_only (bool): If True, only the IDs of the notes are returned.

    Returns:
        JSONResponse: JSON response containing serialized notes or error details.
    
    Raises:
        HTTPException: If the department or course does not exist.
    """
    try:
        # Get the notes for the specified department and course.
        notes = await get_notes_for_course_from_db(
            db_conn_pool, department, course, not ids_only
        )
        # Serialize the notes.
        serializable_notes = create_serializable_notes(notes)
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

@app.post("/get_notes_for_course")
async def get_notes_for_course(request_data: GetNotesForCourseRequestData):
    """
    Retrieves notes for all sections of a specific course.

    Args:
        request_data (GetNotesForCourseRequestData): The request data containing department and course info.

    Returns:
        JSONResponse: A JSON response containing the serialized notes for the course.
    """
    return await get_serializable_notes_for_department_and_course_strings(
        request_data.department, request_data.course, request_data.ids_only
    )

@app.post("/get_notes_for_department_and_course_string")
async def get_notes_for_department_and_course_string(
    request_data: GetNotesForDepartmentAndCourseStringRequestData
):
    """
    Parses a string representing a department code and course code, 
    then retrieves and serializes notes for that department and course.

    Args:
        request_data (GetNotesForDepartmentAndCourseStringRequestData): The request data containing a department and course string.

    Returns:
        JSONResponse: A JSON response containing the serialized notes for the department and course.
    
    Raises:
        HTTPException: If the department and course string is incorrectly formatted.
    """
    department_and_course_string_split = request_data.department_and_course.strip().split()
    if len(department_and_course_string_split) == 2:
        department = department_and_course_string_split[0]
        course = department_and_course_string_split[1]
    elif len(department_and_course_string_split) == 1:
        department_and_course = department_and_course_string_split[0]
        # If the department code is more than 4 characters, split it into department and course.
        if len(department_and_course) > 4:
            department = department_and_course[:4]
            course = department_and_course[4:]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="department_and_course formatted incorrectly"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department_and_course formatted incorrectly"
        )
    return await get_serializable_notes_for_department_and_course_strings(
        department, course, request_data.ids_only
    )


@app.get("/get_departments")
async def get_departments():
    """
    Retrieves the list of all available department codes.

    Returns:
        JSONResponse: A JSON response containing the department codes.
    """
    departments = await get_department_codes(db_conn_pool)
    # Return the list of departments.
    return JSONResponse(content={"success": True, "data": {"departments": departments}, "message": "Departments Returned Successfully!"}, status_code=200, headers={"X-Error": "Custom Error"})

@app.post("/get_courses")
async def get_courses(request_data: GetCoursesRequestData):
    """
    Retrieves the list of all courses available in a specific department.

    Args:
        request_data (GetCoursesRequestData): The request data containing department info.

    Returns:
        JSONResponse: A JSON response containing the courses for the department.
    
    Raises:
        HTTPException: If the department does not exist.
    """
    try:
        courses = await get_courses_for_department(db_conn_pool, request_data.department)
        return JSONResponse(content={"success": True, "data": {"courses": courses}, "message": "Courses Returned Successfully!"}, status_code=200, headers={"X-Error": "Custom Error"})
    
    except DepartmentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department does not exist"
        ) from exc

@app.post("/get_sections")
async def get_sections(request_data: GetSectionsRequestData):
    """
    Retrieves the list of all sections for a specific course in a department.

    Args:
        request_data (GetSectionsRequestData): The request data containing department and course info.

    Returns:
        JSONResponse: A JSON response containing the sections for the course.
    
    Raises:
        HTTPException: If the department or course does not exist.
    """
    try:
        sections = await get_sections_for_course(
            db_conn_pool, request_data.department, request_data.course
        )
        serializable_sections = []
        # Serialize each section for the response.
        for section in sections:
            serializable_sections.append(
                {
                    "id": section.section_id,
                    "instructor": section.instructor,
                    "year": section.year,
                    "semester": section.semester
                }
            )
        return JSONResponse(content={"success": True, "data": {"sections": serializable_sections}, "message": "Sections Returned Successfully!"}, status_code=200, headers={"X-Error": "Custom Error"})
    
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
    current_user: Annotated[User, Depends(get_current_user)], file: UploadFile, section_id: int = Form(...),
):
    """
    Uploads a note for a specific section.

    Args:
        current_user (User): The user uploading the note.
        file (UploadFile): The file to be uploaded.
        section_id (int): The section ID for which the note is uploaded.

    Returns:
        JSONResponse: A JSON response with the note ID.
    
    Raises:
        HTTPException: If the section does not exist.
    """
    try:
        content = await file.read(file.size)
        note_id = await store_note(
            db_conn_pool, section_id, content, file.content_type, current_user.email
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
    Deletes a specific note by its ID.

    Args:
        current_user (User): The user attempting to delete the note.
        request_data (DeleteNoteRequestData): The request data containing the note ID.

    Returns:
        JSONResponse: A JSON response confirming the deletion.
    
    Raises:
        HTTPException: If the note does not exist or if the user is not authorized to delete it.
    """
    try:
        await delete_note_from_db(
            db_conn_pool, request_data.note_id, current_user.email
        )
        return JSONResponse(content={"success": True, "message": f"Note id {request_data.note_id} Deleted Successfully!"}, status_code=200, headers={"X-Error": "Custom Error"})
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
    Attempts to get the note with the specified ID.

    Args:
        request_data (GetNoteRequestData): The request data containing the note ID.

    Returns:
        JSONResponse: A JSON response with the note's details.

    Raises:
        HTTPException: If the note does not exist, a 400 status code with an error message is raised.
    """
    try:
        note = await get_note_from_db(
            db_conn_pool, request_data.note_id
        )
        serializable_note = create_serializable_note(note)
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

    Args:
        request_data (GetNotesForSectionRequestData): The request data containing the section ID and an optional flag for fetching only IDs.

    Returns:
        JSONResponse: A JSON response with the list of notes for the specified section.

    Raises:
        HTTPException: If the section does not exist, a 400 status code with an error message is raised.
    """
    try:
        notes = await get_notes_for_section_from_db(
            db_conn_pool, request_data.section_id, not request_data.ids_only
        )
        serializable_notes = create_serializable_notes(notes)
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
    Attempts to get all the user's notes.

    Args:
        current_user (User): The current authenticated user.
        request_data (GetMyNotesRequestData): The request data containing an optional flag for fetching only IDs.

    Returns:
        JSONResponse: A JSON response with the list of notes for the current user.
    """
    notes = await get_notes_for_user(
        db_conn_pool, current_user.email, not request_data.ids_only
    )
    serializable_notes = create_serializable_notes(notes)
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
    Attempts to leave a rating from a particular user on a particular note.

    Args:
        current_user (User): The current authenticated user.
        request_data (RateNoteRequestData): The request data containing the note ID and rating.

    Returns:
        None: If successful, the rating is updated in the database.
    
    Raises:
        HTTPException: If the rating is not between 1 and 10, or if the note does not exist, a 400 status code with an error message is raised.
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


@app.post("/get_average_note_rating")
async def get_average_note_rating(
    request_data: GetAverageNoteRatingRequestData
):
    """
    Attempts to fetch the average rating of the note with the specified ID, or null if no such ratings exist.

    Args:
        request_data (GetAverageNoteRatingRequestData): The request data containing the note ID.

    Returns:
        JSONResponse: A JSON response with the average rating of the note.
    
    Raises:
        HTTPException: If the note does not exist, a 400 status code with an error message is raised.
    """
    try:
        average_rating = await get_average_note_rating_from_db(
            db_conn_pool, request_data.note_id
        )
        return JSONResponse(
            content = {
                "average_rating": average_rating
            }
        )
    except NoteDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="note does not exist"
        ) from exc


@app.post("/leave_comment")
async def leave_comment(
    current_user: Annotated[User, Depends(get_current_user)],
    request_data: LeaveCommentRequestData
):
    """
    Attempts to leave a comment from a particular user on a particular note, possibly in reply to an existing comment on that note.

    Args:
        current_user (User): The current authenticated user.
        request_data (LeaveCommentRequestData): The request data containing the note ID, parent comment ID, and the content of the comment.

    Returns:
        JSONResponse: A JSON response with the ID of the newly created comment.
    
    Raises:
        HTTPException: If the note or parent comment does not exist, a 400 status code with an error message is raised.
    """
    print("Received request data:", request_data)  # Debug: print incoming request data

    try:
        new_note_id = await leave_comment_on_note(
            db_conn_pool,
            current_user.email,
            request_data.note_id,
            request_data.parent_com_id,
            request_data.content
        )
        return JSONResponse(
            content = {
                "id": new_note_id
            }
        )
    except NoteDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="note does not exist"
        ) from exc
    except ParentCommentDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="parent comment does not exist"
        ) from exc


@app.post("/get_comments_for_note")
async def get_comments_for_note(
    request_data: GetCommentsForNoteRequestData
):
    """
    Attempts to get all comments for the note with the specified ID.

    Args:
        request_data (GetCommentsForNoteRequestData): The request data containing the note ID.

    Returns:
        JSONResponse: A JSON response with a list of comments for the specified note.

    Raises:
        HTTPException: If the note does not exist, a 400 status code with an error message is raised.
    """
    try:
        comments = await get_comments_for_note_from_db(
            db_conn_pool, request_data.note_id
        )
        serializable_comments = []
        for comment in comments:
            serializable_comments.append(
                {
                    "id": comment.comment_id,
                    "note_id": comment.note_id,
                    "parent_comment_id": comment.parent_comment_id,
                    "commenter_id": comment.commenter_id,
                    "content": comment.content,
                }
            )
        return JSONResponse(
            content = {
                "comments": serializable_comments
            }
        )
    except NoteDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="note does not exist"
        ) from exc


@app.post("/get_comment_summary")
async def get_comment_summary(request_data: GetCommentsForNoteRequestData):
    """
    Fetches the top key phrases from the comments on a specific note.

    Args:
        request_data (GetCommentsForNoteRequestData): The request data containing the note ID for which to fetch comments.

    Returns:
        JSONResponse: A JSON response with the extracted key phrases from the comments.
    """
    res = await get_top_keyphrases_from_note_comments(db_conn_pool, request_data.note_id)
    return JSONResponse(content={"success": True, "data": res}, status_code=200, headers={"X-Error": "Custom Error"})


@app.post("/get_role_given_email")
async def get_role_given_email(request_data: GetRoleGivenEmailRequestData):
    """
    Attempts to get the role of a given user with the specified email.

    Args:
        request_data (GetRoleGivenEmailRequestData): The request data containing the email.

    Returns:
        JSONResponse: A JSON response with the user's role.
    
    Raises:
        HTTPException: If the user does not exist, a 400 status code with an error message is raised.
    """
    try:
        role = await get_role_given_email_from_db(db_conn_pool, request_data.email)
        return JSONResponse(
            content = {
                "role": role
            }
        )
    except UserDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user does not exist"
        ) from exc


@app.post("/get_role_given_user_id")
async def get_role_given_user_id(request_data: GetRoleGivenUserIdRequestData):
    """
    Attempts to get the role of a given user with the specified ID.

    Args:
        request_data (GetRoleGivenUserIdRequestData): The request data containing the user ID.

    Returns:
        JSONResponse: A JSON response with the user's role.
    
    Raises:
        HTTPException: If the user does not exist, a 400 status code with an error message is raised.
    """
    try:
        role = await get_role_given_user_id_from_db(db_conn_pool, request_data.user_id)
        return JSONResponse(
            content = {
                "role": role
            }
        )
    except UserDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user does not exist"
        ) from exc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
