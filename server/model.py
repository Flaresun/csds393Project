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
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    """
    Represents full user data in database
    """
<<<<<<< HEAD
    hashed_password: str
=======
    hashed_password: str
>>>>>>> backend
