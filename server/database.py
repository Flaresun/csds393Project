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
                    role = result[2],
                    password_hash = result[3]
                )

async def create_new_user(db_conn_poll, email, password_hash, user_role):
    """
    Attempts to create a new user with the given email, password has and user role;
    raises a UserAlreadyExistsException if a user with that email already exists
    """
    async with db_conn_poll.connection() as conn:
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
