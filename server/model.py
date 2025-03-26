"""
Contains data models for HTTP requests and responses
"""

from pydantic import BaseModel

class Token(BaseModel):
    """
    Represents an OAuth2 bearer token which we return to the user after authentication
    """
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """
    Represents a username contained in a JWT token
    """
    username: str | None = None

class User(BaseModel):
    """
    Represents user data that can be returned to user
    """
    email: str
    id: int
    role: str

class UserInDB(User):
    """
    Represents full user data in database
    """
    password_hash: str

class SignUpRequestData(BaseModel):
    """
    Represents the data contained in a /sign_up request
    """
    email: str
    password: str
    role: str

class CreateCourseRequestData(BaseModel):
    """
    Represents the data contained in a /create_course request
    """
    department: str
    code: str
    name: str

class CreateSectionRequestData(BaseModel):
    """
    Represents the data contained in a /create_section request
    """
    department: str
    course: str
    instructor: str
    year: int
    semester: str

class UploadNoteRequestData(BaseModel):
    """
    Represents data contained in a /upload_note request
    """
    section_id: int
    content: str

class GetNotesForCourseRequestData(BaseModel):
    """
    Represents data contained in a /get_notes_for_course request
    """
    department: str
    course: str
    ids_only: bool

class GetCoursesRequestData(BaseModel):
    """
    Represents data contained in a /get_courses request
    """
    department: str

class GetSectionsRequestData(BaseModel):
    """
    Represents data contained in a /get_sections request
    """
    department: str
    course: str

class DeleteNoteRequestData(BaseModel):
    """
    Represents data contained in a /delete_note request
    """
    note_id: int

class GetNoteRequestData(BaseModel):
    """
    Represents data contained in a /get_note request
    """
    note_id: int

class GetNotesForSectionRequestData(BaseModel):
    """
    Represents data contained in a /get_notes_for_section request
    """
    section_id: int
    ids_only: bool

class GetMyNotesRequestData(BaseModel):
    """
    Represents data contained in a /get_my_notes request
    """
    ids_only: bool
