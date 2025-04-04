import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from psycopg.errors import UniqueViolation, CheckViolation, ForeignKeyViolation
import database
from database import (
    UserAlreadyExistsException,
    DepartmentDoesNotExistException,
    CourseAlreadyExistsException,
    CourseDoesNotExistException,
    FacultyDoesNotExistException,
    UnknownEmptyResultException,
    InvalidSemesterException,
    SectionAlreadyExistsException,
    UserDoesNotExistException,
    SectionDoesNotExistException
)

@pytest.fixture
def mock_db():
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_cur = AsyncMock()

    mock_conn.cursor.return_value.__aenter__.return_value = mock_cur
    mock_pool.connection.return_value.__aenter__.return_value = mock_conn

    return mock_pool, mock_conn, mock_cur

@pytest.mark.asyncio
async def test_get_user(mock_db):
    mock_pool, _, mock_cur = mock_db
    mock_cur.fetchone.return_value = (1, "test@example.com", "hashed_pw", "student")

    user = await database.get_user(mock_pool, "test@example.com")

    assert user.email == "test@example.com"
    assert user.id == 1
    assert user.password_hash == "hashed_pw"
    assert user.role == "student"

    # user is not in the database
    user = await database.get_user(mock_pool, "missing@example.com")

    assert user is None

@pytest.mark.asyncio
async def test_create_new_user(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db

    await database.create_new_user(mock_pool, "new@example.com", "pw", "student")
    mock_cur.execute.assert_called_once()

    # case where user already exists
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = UniqueViolation("duplicate")

    with pytest.raises(UserAlreadyExistsException):
        await database.create_new_user(mock_pool, "dup@example.com", "pw", "student")

@pytest.mark.asyncio
async def test_create_new_course(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db
    mock_cur.fetchone.return_value = (1,)

    await database.create_new_course(mock_pool, "CS", "101", "Intro to CS")
    mock_cur.execute.assert_called()

    # case where course already exists
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = UniqueViolation("duplicate")

    with pytest.raises(CourseAlreadyExistsException):
        await database.create_new_course(mock_pool, "CS", "101", "Intro to CS")

    # case where department doesn't exist
    mock_cur.execute.reset_mock()
    mock_cur.fetchone.return_value = None

    with pytest.raises(DepartmentDoesNotExistException):
        await database.create_new_course(mock_pool, "XX", "101", "Ghost Course")

@pytest.mark.asyncio
async def test_create_new_section(mock_db):
    mock_pool, _, mock_cur = mock_db

    await database.create_new_section(mock_pool, "CS101", "001", "MWF 10-11", "fall", "instructor@example.com")
    mock_cur.execute.assert_called_once_with(
        """
        INSERT INTO sections (course_code, section_number, meeting_times, semester, instructor_email)
        VALUES ($1, $2, $3, $4, $5)
        """,
        "CS101", "001", "MWF 10-11", "fall", "instructor@example.com"
    )

    # course doesn't exist
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = CourseDoesNotExistException("course doesn't exist")

    with pytest.raises(CourseDoesNotExistException):
        await database.create_new_section(mock_pool, "BAD101", "001", "MWF 10-11", "fall", "instructor@example.com")

    # faculty doesn't exist
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = FacultyDoesNotExistException("not a faculty member")

    with pytest.raises(FacultyDoesNotExistException):
        await database.create_new_section(mock_pool, "CS101", "001", "MWF 10-11", "fall", "not_faculty@example.com")

    # unknown empty result
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = UnknownEmptyResultException("unexpected None result")

    with pytest.raises(UnknownEmptyResultException):
        await database.create_new_section(mock_pool, "CS101", "001", "MWF 10-11", "fall", "faculty@example.com")

    # semester is invalid
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = InvalidSemesterException("not a valid semester")

    with pytest.raises(InvalidSemesterException):
        await database.create_new_section(mock_pool, "CS101", "001", "MWF 10-11", "winter", "faculty@example.com")

    # section already exists
    mock_cur.execute.reset_mock()
    mock_cur.execute.side_effect = SectionAlreadyExistsException("duplicate section")

    with pytest.raises(SectionAlreadyExistsException):
        await database.create_new_section(mock_pool, "CS101", "001", "MWF 10-11", "fall", "faculty@example.com")

@pytest.mark.asyncio
async def test_store_note(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db
    mock_cur.fetchone.return_value = (42,)

    note_id = await database.store_note(mock_pool, 1, "My note", "student@example.com")
    assert note_id == 42

    # user doesn't exist
    mock_cur.fetchone.return_value = None
    with pytest.raises(UserDoesNotExistException):
        await database.store_note(mock_pool, 1, "My note", "ghost@example.com")

    # section doesn't exist
    mock_cur.execute.side_effect = ForeignKeyViolation("fk")
    with pytest.raises(SectionDoesNotExistException):
        await database.store_note(mock_pool, 999, "My note", "user@example.com")

@pytest.mark.asyncio
async def test_get_notes_for_course(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db

    mock_cur.fetchall.return_value = [
        (1, 101, 201, "Note content 1"),
        (2, 102, 202, "Note content 2")
    ]
    notes = await database.get_notes_for_course(mock_pool, "CS", "101", get_content=True)
    assert len(notes) == 2
    assert notes[0].note_id == 1
    assert notes[1].content == "Note content 2"

    # department does not exist
    mock_cur.fetchall.return_value = []
    mock_cur.fetchone.return_value = None
    with pytest.raises(DepartmentDoesNotExistException):
        await database.get_notes_for_course(mock_pool, "NONEXISTENT", "101", get_content=True)

    # course doesn't exist
    mock_cur.fetchall.return_value = []
    mock_cur.fetchone.side_effect = [("department_id",), None]
    with pytest.raises(CourseDoesNotExistException):
        await database.get_notes_for_course(mock_pool, "CS", "999", get_content=True)

@pytest.mark.asyncio
async def test_get_department_codes(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db

    mock_cur.fetchall.return_value = [("CS",), ("MATH",)]
    department_codes = await database.get_department_codes(mock_pool)
    assert department_codes == ["CS", "MATH"]

    # no departments
    mock_cur.fetchall.return_value = []
    department_codes = await database.get_department_codes(mock_pool)
    assert department_codes == []

@pytest.mark.asyncio
async def test_get_courses_for_department(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db

    mock_cur.fetchall.return_value = [("101",), ("102",)]
    course_codes = await database.get_courses_for_department(mock_pool, "CS")
    assert course_codes == ["101", "102"]

    # department doesn't exist
    mock_cur.fetchall.return_value = []
    mock_cur.fetchone.return_value = None
    with pytest.raises(DepartmentDoesNotExistException):
        await database.get_courses_for_department(mock_pool, "NONEXISTENT")

@pytest.mark.asyncio
async def test_get_section_ids_for_course(mock_db):
    mock_pool, mock_conn, mock_cur = mock_db

    mock_cur.fetchall.return_value = [(201,), (202,)]
    section_ids = await database.get_section_ids_for_course(mock_pool, "CS", "101")
    assert section_ids == [201, 202]

    # department doesn't exist
    mock_cur.fetchall.return_value = []
    mock_cur.fetchone.return_value = None
    with pytest.raises(DepartmentDoesNotExistException):
        await database.get_section_ids_for_course(mock_pool, "NONEXISTENT", "101")

    # course doesn't exist
    mock_cur.fetchall.return_value = []
    mock_cur.fetchone.side_effect = [("department_id",), None]
    with pytest.raises(CourseDoesNotExistException):
        await database.get_section_ids_for_course(mock_pool, "CS", "999")
