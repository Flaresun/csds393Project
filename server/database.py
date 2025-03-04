"""
Methods for interfacing with the database.
"""

from psycopg.errors import UniqueViolation

from model import UserInDB

class UserAlreadyExistsException(Exception):
    """
    Raised when someone attempts to create a new user with an email that is already in use
    """

async def get_user(db_conn_pool, email: str):
    """
    Get information about the user with the given email from the database, or return None
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, email, password_hash, user_role FROM users
                WHERE email = %s
                """,
                (email,)
            )
            result = await cur.fetchone()
            if result is not None:
                return UserInDB(
                    email = result[1],
                    id = result[0],
                    password_hash = result[2],
                    role = result[3],
                )

async def create_new_user(db_conn_pool, email, password_hash, user_role):
    """
    Attempts to create a new user with the given email, password has and user role;
    raises a UserAlreadyExistsException if a user with that email already exists
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    """
                    INSERT INTO users (email, password_hash, user_role)
                    VALUES (%s, %s, %s)
                    """,
                    (email, password_hash, user_role)
                )
            except UniqueViolation as exc:
                raise UserAlreadyExistsException() from exc

class DepartmentDoesNotExistException(Exception):
    """
    Raised when a faculty member attempts to create a course in a department that does not exist
    """

class CourseAlreadyExistsException(Exception):
    """
    Raised when a faculty member attempts to create a course that already exists
    """

async def create_new_course(db_conn_pool, department_code, code, name):
    """
    Attempts to create a new course with the specified code and name in the specified department.
    Raises a DepartmentDoesNotExistException if the specified department does not exist, and a
    CourseAlreadyExists exception if the course already exists.
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    """
                    WITH department AS (
                        SELECT id FROM departments WHERE code = %s
                    )
                    INSERT INTO courses (department_id, code, name)
                    SELECT department.id, %s, %s
                    FROM department
                    RETURNING id
                    """,
                    (department_code.upper(), code.upper(), name)
                )
                # If we are trying to create a course that already exists, then the insertion will
                # raise a UniqueViolation.
                # If the result is None, then the specified department does not exist and we throw
                # the corresponding error.
                # Otherwise, we have successfully created the new course.
                result = await cur.fetchone()
                if result is None:
                    raise DepartmentDoesNotExistException()
            except UniqueViolation as exc:
                raise CourseAlreadyExistsException() from exc
