import pytest
from unittest.mock import AsyncMock, MagicMock

import database
from model import Section
from server.model import UserInDB

# Fixture for creating mocked database connection, cursor, and pool
@pytest.fixture
def mock_db_pool():
    """
    Fixture to create a mocked database pool, connection, and cursor.
    """
    mock_cursor = AsyncMock()
    mock_cursor.execute = AsyncMock()
    mock_cursor.fetchone = AsyncMock()
    mock_cursor.fetchall = AsyncMock()

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

    mock_db_pool = MagicMock()
    mock_db_pool.connection.return_value.__aenter__.return_value = mock_conn

    return {
        "pool": mock_db_pool,
        "conn": mock_conn,
        "cursor": mock_cursor,
    }

@pytest.mark.asyncio
async def test_get_user_found(mock_db_pool):
    """
    Test that an existing user is successfully retrieved from the database.
    """
    mock_db_pool["cursor"].fetchone.return_value = (
        1, "test@example.com", "hash123", "student"
    )
    user = await database.get_user(mock_db_pool["pool"], "test@example.com")
    assert user.email == "test@example.com"
    assert user.password_hash == "hash123"
    assert user.role == "student"

@pytest.mark.asyncio
async def test_get_user_not_found(mock_db_pool):
    """
    Test that None is returned when the user is not found in the database.
    """
    mock_db_pool["cursor"].fetchone.return_value = None
    user = await database.get_user(mock_db_pool["pool"], "notfound@example.com")
    assert user is None

@pytest.mark.asyncio
async def test_create_new_user_success(mock_db_pool):
    """
    Test that a new user can be successfully created.
    """
    await database.create_new_user(mock_db_pool["pool"], "new@example.com", "pw123", "student")
    mock_db_pool["cursor"].execute.assert_called()

@pytest.mark.asyncio
async def test_create_new_user_unique_violation(mock_db_pool):
    """
    Test that creating a duplicate user raises UserAlreadyExistsException.
    """
    mock_db_pool["cursor"].execute.side_effect = database.UniqueViolation()
    with pytest.raises(database.UserAlreadyExistsException):
        await database.create_new_user(mock_db_pool["pool"], "dup@example.com", "pw", "student")

@pytest.mark.asyncio
async def test_create_new_course_department_missing(mock_db_pool):
    """
    Test that creating a course with a non-existent department raises DepartmentDoesNotExistException.
    """
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.DepartmentDoesNotExistException):
        await database.create_new_course(mock_db_pool["pool"], "X", "CS101", "Intro to CS")

@pytest.mark.asyncio
async def test_create_new_course_unique_violation(mock_db_pool):
    """
    Test that creating a duplicate course raises CourseAlreadyExistsException.
    """
    mock_db_pool["cursor"].execute.side_effect = database.UniqueViolation()
    with pytest.raises(database.CourseAlreadyExistsException):
        await database.create_new_course(mock_db_pool["pool"], "CS", "CS101", "Intro to CS")

@pytest.mark.asyncio
async def test_create_new_section_invalid_semester(mock_db_pool):
    """
    Test that creating a section with an invalid semester raises InvalidSemesterException.
    """
    mock_db_pool["cursor"].execute.side_effect = database.CheckViolation()
    with pytest.raises(database.InvalidSemesterException):
        await database.create_new_section(
            mock_db_pool["pool"], "CS", "CS101", "prof@example.com", 2025, "invalid"
        )

@pytest.mark.asyncio
async def test_store_note_success(mock_db_pool):
    """
    Test that a note is stored and its ID is returned on success.
    """
    mock_db_pool["cursor"].fetchone.return_value = (42,)
    result = await database.store_note(
        mock_db_pool["pool"], section_id=1, content=b"note content",
        content_type="text", email="student@example.com"
    )
    assert result == 42

@pytest.mark.asyncio
async def test_store_note_user_does_not_exist(mock_db_pool):
    """
    Test that storing a note with an unknown user raises UserDoesNotExistException.
    """
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.UserDoesNotExistException):
        await database.store_note(
            mock_db_pool["pool"], section_id=1, content=b"note content",
            content_type="text", email="ghost@example.com"
        )

@pytest.mark.asyncio
async def test_store_note_section_fk_violation(mock_db_pool):
    """
    Test that storing a note with an invalid section raises SectionDoesNotExistException.
    """
    mock_db_pool["cursor"].execute.side_effect = database.ForeignKeyViolation()
    with pytest.raises(database.SectionDoesNotExistException):
        await database.store_note(
            mock_db_pool["pool"], section_id=999, content=b"note content",
            content_type="text", email="student@example.com"
        )

def test_get_notes_from_results_with_content():
    """
    Test that get_notes_from_results returns notes with content when requested.
    """
    results = [(1, 2, 3, "text/plain", b"note content")]
    notes = database.get_notes_from_results(results, get_content=True)
    assert len(notes) == 1
    assert isinstance(notes[0], database.Note)
    assert notes[0].content == b"note content"
    assert notes[0].content_type == "text/plain"

def test_get_notes_from_results_without_content():
    """
    Test that get_notes_from_results returns notes without content when not requested.
    """
    results = [(1, 2, 3, "text/plain", b"note content")]
    notes = database.get_notes_from_results(results, get_content=False)
    assert len(notes) == 1
    assert notes[0].content is None

@pytest.mark.asyncio
async def test_get_notes_for_course_found(mock_db_pool):
    """
    Test that notes for a given course are retrieved successfully.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(1, 2, 3, "text/plain", b"note")]
    notes = await database.get_notes_for_course(mock_db_pool["pool"], "CS", "CS101", get_content=True)
    assert isinstance(notes[0], database.Note)

@pytest.mark.asyncio
async def test_get_notes_for_course_dept_not_found(mock_db_pool):
    """
    Test that DepartmentDoesNotExistException is raised when the department is not found.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.side_effect = [None]
    with pytest.raises(database.DepartmentDoesNotExistException):
        await database.get_notes_for_course(mock_db_pool["pool"], "BAD", "CS101", True)

@pytest.mark.asyncio
async def test_get_notes_for_course_course_not_found(mock_db_pool):
    """
    Test that CourseDoesNotExistException is raised when the course is not found.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.side_effect = [(1,), None]
    with pytest.raises(database.CourseDoesNotExistException):
        await database.get_notes_for_course(mock_db_pool["pool"], "CS", "FAKE", False)

@pytest.mark.asyncio
async def test_get_department_codes(mock_db_pool):
    """
    Test that department codes are retrieved successfully.
    """
    mock_db_pool["cursor"].fetchall.return_value = [("CS",), ("MATH",)]
    result = await database.get_department_codes(mock_db_pool["pool"])
    assert result == ["CS", "MATH"]

@pytest.mark.asyncio
async def test_get_courses_for_department_success(mock_db_pool):
    """
    Test that courses for a department are retrieved successfully.
    """
    mock_db_pool["cursor"].fetchall.return_value = [("CS101",), ("CS102",)]
    result = await database.get_courses_for_department(mock_db_pool["pool"], "CS")
    assert result == ["CS101", "CS102"]

@pytest.mark.asyncio
async def test_get_courses_for_department_dept_not_found(mock_db_pool):
    """
    Test that DepartmentDoesNotExistException is raised when department is missing.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.DepartmentDoesNotExistException):
        await database.get_courses_for_department(mock_db_pool["pool"], "UNKNOWN")

@pytest.mark.asyncio
async def test_get_sections_for_course_found(mock_db_pool):
    """
    Test that sections for a course are returned correctly.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(1, "prof@example.com", 2023, "fall")]
    result = await database.get_sections_for_course(mock_db_pool["pool"], "CS", "CS101")
    assert isinstance(result[0], Section)
    assert result[0].instructor == "prof@example.com"

@pytest.mark.asyncio
async def test_get_sections_for_course_dept_not_found(mock_db_pool):
    """
    Test that DepartmentDoesNotExistException is raised for an unknown department.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.DepartmentDoesNotExistException):
        await database.get_sections_for_course(mock_db_pool["pool"], "BAD", "CS101")

@pytest.mark.asyncio
async def test_get_sections_for_course_course_not_found(mock_db_pool):
    """
    Test that CourseDoesNotExistException is raised for an unknown course.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.side_effect = [(1,), None]
    with pytest.raises(database.CourseDoesNotExistException):
        await database.get_sections_for_course(mock_db_pool["pool"], "CS", "UNKNOWN")

@pytest.mark.asyncio
async def test_delete_note_success(mock_db_pool):
    """
    Test that a note is deleted successfully.
    """
    mock_db_pool["cursor"].rowcount = 1
    await database.delete_note(mock_db_pool["pool"], note_id=1, email="owner@example.com")
    mock_db_pool["cursor"].execute.assert_called()

@pytest.mark.asyncio
async def test_delete_note_not_found(mock_db_pool):
    """
    Test that NoteDoesNotExistException is raised if the note is missing.
    """
    mock_db_pool["cursor"].rowcount = 0
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.NoteDoesNotExistException):
        await database.delete_note(mock_db_pool["pool"], note_id=99, email="user@example.com")

@pytest.mark.asyncio
async def test_delete_note_permission_denied(mock_db_pool):
    """
    Test that UserIsNotOwnerOrFacultyException is raised if the user is not allowed to delete the note.
    """
    mock_db_pool["cursor"].rowcount = 0
    mock_db_pool["cursor"].fetchone.side_effect = [
        (99, 1, 2, b"content", "text/plain"),
        (1, "student")
    ]
    with pytest.raises(database.UserIsNotOwnerOrFacultyException):
        await database.delete_note(mock_db_pool["pool"], note_id=1, email="nonowner@example.com")

@pytest.mark.asyncio
async def test_get_note_success(mock_db_pool):
    """
    Test that a specific note is retrieved successfully by ID.
    """
    mock_db_pool["cursor"].fetchone.return_value = (1, 2, 3, b"data", "text/plain")
    note = await database.get_note(mock_db_pool["pool"], 1)
    assert note.note_id == 1
    assert note.content == b"data"

@pytest.mark.asyncio
async def test_get_note_not_found(mock_db_pool):
    """
    Test that NoteDoesNotExistException is raised if a note is not found.
    """
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.NoteDoesNotExistException):
        await database.get_note(mock_db_pool["pool"], 123)

@pytest.mark.asyncio
async def test_get_notes_for_section_with_results(mock_db_pool):
    """
    Test that notes for a specific section are returned when available.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(1, 2, 3, "text/plain", b"abc")]
    notes = await database.get_notes_for_section(mock_db_pool["pool"], section_id=5, get_content=True)
    assert len(notes) == 1
    assert notes[0].section_id == 2

@pytest.mark.asyncio
async def test_get_notes_for_section_not_found(mock_db_pool):
    """
    Test that SectionDoesNotExistException is raised when the section is invalid.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.SectionDoesNotExistException):
        await database.get_notes_for_section(mock_db_pool["pool"], section_id=999, get_content=False)

@pytest.mark.asyncio
async def test_get_notes_for_user_with_results(mock_db_pool):
    """
    Test that a user's notes are returned correctly.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(1, 2, 3, "text/plain", b"note")]
    notes = await database.get_notes_for_user(mock_db_pool["pool"], email="a@b.com", get_content=True)
    assert isinstance(notes[0], database.Note)

@pytest.mark.asyncio
async def test_set_or_update_note_rating_success(mock_db_pool):
    """
    Test that setting or updating a note rating completes without error.
    """
    await database.set_or_update_note_rating(mock_db_pool["pool"], "rater@example.com", 1, 5)
    mock_db_pool["cursor"].execute.assert_called()

@pytest.mark.asyncio
async def test_set_or_update_note_rating_note_not_found(mock_db_pool):
    """
    Test that NoteDoesNotExistException is raised if a rated note does not exist.
    """
    mock_db_pool["cursor"].execute.side_effect = [
        database.ForeignKeyViolation(),
        None
    ]
    mock_db_pool["cursor"].fetchone.return_value = None
    mock_db_pool["conn"].rollback = AsyncMock()

    with pytest.raises(database.NoteDoesNotExistException):
        await database.set_or_update_note_rating(
            mock_db_pool["pool"], "user@example.com", 42, 5
        )

@pytest.mark.asyncio
async def test_get_average_note_rating_success(mock_db_pool):
    """
    Test that the correct average rating is returned for a rated note.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(4.5,)]
    result = await database.get_average_note_rating(mock_db_pool["pool"], note_id=1)
    assert result == 4.5

@pytest.mark.asyncio
async def test_get_average_note_rating_unrated_note(mock_db_pool):
    """
    Test that None is returned when a note has no ratings.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(None,)]
    mock_db_pool["cursor"].fetchone.return_value = (1, 2, 3, b"abc", "text/plain")
    result = await database.get_average_note_rating(mock_db_pool["pool"], note_id=100)
    assert result is None

@pytest.mark.asyncio
async def test_get_average_note_rating_note_not_found(mock_db_pool):
    """
    Test that NoteDoesNotExistException is raised when the note is missing.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(None,)]
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.NoteDoesNotExistException):
        await database.get_average_note_rating(mock_db_pool["pool"], note_id=200)

@pytest.mark.asyncio
async def test_leave_comment_on_note_top_level(mock_db_pool):
    """
    Test that a top-level comment is successfully created and returns its ID.
    """
    mock_db_pool["cursor"].fetchone.return_value = (123,)
    result = await database.leave_comment_on_note(
        mock_db_pool["pool"], "a@b.com", 1, None, "Nice note"
    )
    assert result == 123

@pytest.mark.asyncio
async def test_leave_comment_on_note_reply_to_missing_parent(mock_db_pool):
    """
    Test that replying to a non-existent parent comment raises ParentCommentDoesNotExistException.
    """
    mock_db_pool["cursor"].fetchone.side_effect = [None, None]
    with pytest.raises(database.ParentCommentDoesNotExistException):
        await database.leave_comment_on_note(
            mock_db_pool["pool"], "a@b.com", 1, 999, "Replying"
        )

@pytest.mark.asyncio
async def test_get_comments_for_note_found(mock_db_pool):
    """
    Test that comments for a note are retrieved correctly.
    """
    mock_db_pool["cursor"].fetchall.return_value = [(1, 1, None, 2, "hello")]
    comments = await database.get_comments_for_note(mock_db_pool["pool"], 1)
    assert comments[0].content == "hello"

@pytest.mark.asyncio
async def test_get_comments_for_note_not_found(mock_db_pool):
    """
    Test that NoteDoesNotExistException is raised when no comments or note exist.
    """
    mock_db_pool["cursor"].fetchall.return_value = []
    mock_db_pool["cursor"].fetchone.return_value = None
    with pytest.raises(database.NoteDoesNotExistException):
        await database.get_comments_for_note(mock_db_pool["pool"], 1)