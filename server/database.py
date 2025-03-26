"""
Methods for interfacing with the database.
"""

from psycopg.errors import CheckViolation, ForeignKeyViolation, UniqueViolation

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
    Raised when we attempt to perform an operation using a department that does not exist
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

class CourseDoesNotExistException(Exception):
    """
    Raised when we attempt to perform an operation using a course that does not exist
    """

class FacultyDoesNotExistException(Exception):
    """
    Raised when a faculty member attempts to create a course having an instructor that is not a
    user with the 'faculty' role
    """

class UnknownEmptyResultException(Exception):
    """
    Raised when a query that should have returned a result instead returned None, and we are unable
    to determine why.
    """

class InvalidSemesterException(Exception):
    """
    Raised when a faculty member attempts to create a section in an invalid semester (valid are
    'fall', 'spring', 'summer')
    """

class SectionAlreadyExistsException(Exception):
    """
    Raised when a faculty member attempts to create a section that already exists
    """

async def create_new_section(db_conn_pool, department, course, instructor, year, semester):
    """
    Attempts to create a new section.
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    """
                    WITH department AS (
                        SELECT id FROM departments WHERE code = %s
                    ),
                    course AS (
                        SELECT courses.id FROM courses, department 
                        WHERE department_id = department.id AND code = %s
                    ),
                    faculty AS (
                        SELECT id FROM users WHERE email = %s AND user_role = 'faculty'
                    )
                    INSERT INTO sections (course_id, instructor, year, semester)
                    SELECT course.id, faculty.id, %s, %s
                    FROM course, faculty
                    RETURNING id
                    """,
                    (department.upper(), course.upper(), instructor, year, semester.lower())
                )
                # If we are trying to create a section that already exists, then the insertion will
                # raise a UniqueViolation
                # If the result is None, then either the specified department doesn't exist, the
                # specified course doesn't exist, or a user with the specified email and the
                # faculty role doesn't exist.
                # Otherwise, we have successfully created the new section.
                result = await cur.fetchone()
                if result is None:
                    # First, we check if the department exists.
                    await cur.execute(
                        """
                        SELECT id FROM departments WHERE code = %s
                        """,
                        (department,)
                    )
                    result = await cur.fetchone()
                    if result is None:
                        raise DepartmentDoesNotExistException()
                    department_id = result[0]
                    # Next, we check if the specified course exists
                    await cur.execute(
                        """
                        SELECT id FROM courses WHERE department_id = %s AND code = %s
                        """,
                        (department_id, course.upper())
                    )
                    result = await cur.fetchone()
                    if result is None:
                        raise CourseDoesNotExistException()
                    # Finally, we check if a faculty member with the specified email exists
                    await cur.execute(
                        """
                        SELECT email FROM users WHERE email = %s AND user_role = 'faculty'
                        """,
                        (instructor,)
                    )
                    result = await cur.fetchone()
                    if result is None:
                        raise FacultyDoesNotExistException()
                    # Something else went wrong, but we don't know what.
                    raise UnknownEmptyResultException()
                return result[0]
            except CheckViolation as exc:
                print(exc)
                raise InvalidSemesterException() from exc
            except UniqueViolation as exc:
                raise SectionAlreadyExistsException() from exc

class UserDoesNotExistException(BaseException):
    """
    Raised when we attempt to store a note belonging to a user that does not exist
    """

class SectionDoesNotExistException(BaseException):
    """
    Raised when a user attempts to reference a section that does not exist
    """

async def store_note(db_conn_pool, section_id, content, email):
    """
    Attempts to store a note.
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    """
                    WITH owner AS (
                        SELECT id FROM users WHERE email = %s
                    )
                    INSERT INTO notes (section_id, owner_id, content)
                    SELECT %s, owner.id, %s
                    FROM owner
                    RETURNING id
                    """,
                    (email, section_id, content)
                )
                # If the result is None, then the owner user doesn't exist.
                # Otherwise, we have successfully created the new section.
                result = await cur.fetchone()
                if result is None:
                    raise UserDoesNotExistException()
                return result[0]
            except ForeignKeyViolation as exc:
                raise SectionDoesNotExistException() from exc

class Note:
    """
    Represents a note stored in the database
    """
    def __init__(self, note_id: int, section_id: int, owner_id: int, content: str):
        self.note_id = note_id
        self.section_id = section_id
        self.owner_id = owner_id
        self.content = content

async def get_notes_for_course(db_conn_pool, department, course, get_content):
    """
    Attempts to get all notes for a particular course from all sections
    """
    if get_content:
        note_selection_string = \
            "SELECT notes.id, notes.section_id, notes.owner_id, notes.content FROM notes"
    else:
        note_selection_string = "SELECT notes.id, notes.section_id, notes.owner_id FROM notes"
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"""
                WITH department AS (
                    SELECT id FROM departments WHERE code = %s
                ),
                course AS (
                    SELECT courses.id FROM courses, department
                    WHERE department_id = department.id AND code = %s
                ),
                section_ids AS (
                    SELECT sections.id FROM sections, course WHERE course_id = course.id
                )
                {note_selection_string}
                INNER JOIN section_ids ON notes.section_id = section_ids.id
                """,
                (department.upper(), course.upper())
            )
            results = await cur.fetchall()
            # If we get no results from our query, then perhaps we did query with valid department
            # and course codes, but no notes exist for that particular course. However, an empty
            # result could indicate that we queried with a department and/or course code that does
            # not exist. We check that here
            if len(results) == 0:
                # First, we check if the department exists.
                await cur.execute(
                    """
                    SELECT id FROM departments WHERE code = %s
                    """,
                    (department,)
                )
                result = await cur.fetchone()
                if result is None:
                    raise DepartmentDoesNotExistException()
                department_id = result[0]
                # Next, we check if the specified course exists
                await cur.execute(
                    """
                    SELECT id FROM courses WHERE department_id = %s AND code = %s
                    """,
                    (department_id, course.upper())
                )
                result = await cur.fetchone()
                if result is None:
                    raise CourseDoesNotExistException()
            notes = []
            for result in results:
                if get_content:
                    content = result[3]
                else:
                    content = None
                notes.append(
                    Note(
                        note_id = result[0],
                        section_id = result[1],
                        owner_id = result[2],
                        content = content
                    )
                )
            return notes

async def get_department_codes(db_conn_pool):
    """
    Attempts to get the codes of all available courses
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT code FROM departments
                """
            )
            results = await cur.fetchall()
            department_codes = []
            for result in results:
                department_codes.append(result[0])
            return department_codes

async def get_courses_for_department(db_conn_pool, department_code):
    """
    Attempts to get the codes of all courses in a particular department
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                WITH department AS (
                    SELECT id FROM departments WHERE code = %s
                )
                SELECT courses.code FROM courses, department
                WHERE courses.id = department.id
                """,
                (department_code,)
            )
            results = await cur.fetchall()
            # If we get no results from our query, then either we queried with a valid department
            # code but no courses exist in that department, or we queried with a course code that
            # does not exist. We check that here
            if len(results) == 0:
                await cur.execute(
                    """
                    SELECT id FROM departments WHERE code = %s
                    """,
                    (department_code,)
                )
                result = await cur.fetchone()
                if result is None:
                    raise DepartmentDoesNotExistException()
            course_codes = []
            for result in results:
                course_codes.append(result[0])
            return course_codes

async def get_section_ids_for_course(db_conn_pool, department_code, course_code):
    """
    Attempts to get the section IDs of all sections of a particular course
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                WITH department AS (
                    SELECT id FROM departments WHERE code = %s
                ),
                course AS (
                    SELECT courses.id FROM courses, department
                    WHERE department_id = department.id AND code = %s
                )
                SELECT sections.id FROM sections, course
                WHERE sections.course_id = course.id
                """,
                (department_code.upper(), course_code.upper())
            )
            results = await cur.fetchall()
            # If we get no results from our query, then perhaps we did query with valid department
            # and course codes, but no sections of that course exist. However, an empty result
            # could indicate that we queried with a department and/or course code that does not
            # exist. We check that here.
            if len(results) == 0:
                # First, we check if the department exists.
                await cur.execute(
                    """
                    SELECT id FROM departments WHERE code = %s
                    """,
                    (department_code,)
                )
                result = await cur.fetchone()
                if result is None:
                    raise DepartmentDoesNotExistException()
                department_id = result[0]
                # Next, we check if the specified course exists
                await cur.execute(
                    """
                    SELECT id FROM courses WHERE department_id = %s AND code = %s
                    """,
                    (department_id, course_code.upper())
                )
                result = await cur.fetchone()
                if result is None:
                    raise CourseDoesNotExistException()
            section_ids = []
            for result in results:
                section_ids.append(result[0])
            return section_ids

class NoteDoesNotExistException(BaseException):
    """
    Raised when a user attempts to perform an action on a note that does not exist
    """

class UserIsNotOwnerOrFacultyException(BaseException):
    """
    Used when a user who does not have the faculty role attempts to delete a note they do not own
    """

async def delete_note(db_conn_pool, note_id, email):
    """
    Attempts to delete a note with the specified ID
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                WITH owner AS (
                    SELECT id FROM users WHERE email = %s
                )
                DELETE FROM notes USING owner
                WHERE notes.id = %s AND (
                    owner_id = owner.id OR owner.id IN (
                        SELECT id FROM users WHERE user_role = 'faculty'
                    )
                )
                """,
                (email, note_id)
            )
            num_rows_deleted = cur.rowcount
            # If no rows were deleted, then either we attempted to delete a note that doesn't
            # exist or we attempted to delete a node belonging to a user that is not the calling
            # user and the calling user doesn't have the faculty role. We check that here
            print(num_rows_deleted)
            if num_rows_deleted == 0:
                result = await cur.execute(
                    """
                    SELECT * FROM notes WHERE id = %s
                    """,
                    (note_id,)
                )
                result = await cur.fetchone()
                if result is None:
                    raise NoteDoesNotExistException()
                note_owner_id = result[2]
                # Next, we check if the user is not the owner and doesn't have the faculty role
                result = await cur.execute(
                    """
                    SELECT id, user_role FROM users WHERE email = %s
                    """,
                    (email,)
                )
                result = await cur.fetchone()
                caller_id, caller_role = result[0], result[1]
                if note_owner_id != caller_id and caller_role != 'faculty':
                    raise UserIsNotOwnerOrFacultyException()
                # The note does exist and either the owner is the caller or the caller does have
                # the faculty role, but for some reason the note wasn't deleted.
                raise UnknownEmptyResultException()

async def get_note(db_conn_pool, note_id):
    """
    Attempts to get the note with the specified id
    """
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT * FROM notes WHERE notes.id = %s
                """,
                (note_id,)
            )
            result = await cur.fetchone()
            if result is None:
                raise NoteDoesNotExistException()
            return Note(
                note_id = result[0],
                section_id = result[1],
                owner_id = result[2],
                content = result[3]
            )

async def get_notes_for_section(db_conn_pool, section_id, get_content):
    """
    Attempts to get all notes for a particular section of a course
    """
    if get_content:
        note_selection_string = \
            "SELECT notes.id, notes.section_id, notes.owner_id, notes.content FROM notes"
    else:
        note_selection_string = "SELECT notes.id, notes.section_id, notes.owner_id FROM notes"
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"""
                {note_selection_string}
                WHERE notes.section_id = %s
                """,
                (section_id,)
            )
            results = await cur.fetchall()
            # If we get no results from our query, then perhaps we did query with a valid section
            # id, but no notes exist for that section. However, an empty result could indicate that
            # we queried with a section id that does not exist. We check that here
            if len(results) == 0:
                await cur.execute(
                    """
                    SELECT * FROM sections WHERE id = %s
                    """,
                    (section_id,)
                )
                result = await cur.fetchone()
                if result is None:
                    raise SectionDoesNotExistException()
            notes = []
            for result in results:
                if get_content:
                    content = result[3]
                else:
                    content = None
                notes.append(
                    Note(
                        note_id = result[0],
                        section_id = result[1],
                        owner_id = result[2],
                        content = content
                    )
                )
            return notes

async def get_notes_for_user(
    db_conn_pool, email, get_content
):
    """
    Attempts to get all notes for a particular user
    """
    if get_content:
        note_selection_string = \
            "SELECT notes.id, notes.section_id, notes.owner_id, notes.content FROM notes"
    else:
        note_selection_string = "SELECT notes.id, notes.section_id, notes.owner_id FROM notes"
    async with db_conn_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"""
                WITH owner AS (
                    SELECT id FROM users WHERE email = %s
                )
                {note_selection_string}, owner
                WHERE notes.owner_id = owner.id
                """,
                (email,)
            )
            results = await cur.fetchall()
            notes = []
            for result in results:
                if get_content:
                    content = result[3]
                else:
                    content = None
                notes.append(
                    Note(
                        note_id = result[0],
                        section_id = result[1],
                        owner_id = result[2],
                        content = content
                    )
                )
            return notes
