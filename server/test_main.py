import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from database import (
    UserAlreadyExistsException,
    DepartmentDoesNotExistException,
    CourseDoesNotExistException, Note, SectionDoesNotExistException,
    NoteDoesNotExistException,
    ParentCommentDoesNotExistException,
    UserDoesNotExistException,
)
from main import app, create_serializable_note, create_serializable_notes, \
    get_serializable_notes_for_department_and_course_strings


@pytest_asyncio.fixture
async def client():
    """
    Provides an async test client using FastAPI's ASGI transport for simulating HTTP requests.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.mark.asyncio
class TestMainRoutes:
    """
    Test suite for all public FastAPI endpoints in main.py.
    """

    @pytest_asyncio.fixture(autouse=True)
    async def override_auth_dependencies(self):
        """
        Globally overrides get_current_user for all tests to simulate an authenticated user.
        """
        from main import get_current_user
        app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(email="test@example.com")
        yield
        app.dependency_overrides.clear()

    @pytest.fixture
    def valid_token(self):
        """
        Supplies a reusable mock JWT token.
        """
        return "valid.jwt.token"

    @pytest.fixture
    def mocked_user(self):
        """
        Supplies a mock user object with email and faculty role.
        """
        return type("User", (), {"email": "user@example.com", "role": "faculty"})

    # === /validate_user ===
    @patch("main.get_user", new_callable=AsyncMock)
    @patch("main.jwt.decode")
    async def test_validate_user_success(self, jwt_decode_mock, get_user_mock, client, valid_token, mocked_user):
        """
        Should return 200 if the token is valid and user exists.
        """
        jwt_decode_mock.return_value = {"sub": "user@example.com"}
        get_user_mock.return_value = mocked_user
        headers = {"Authorization": f"Bearer {valid_token}"}

        response = await client.post("/validate_user", headers=headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"] == "user@example.com"

    async def test_validate_user_missing_token(self, client):
        """
        Should return 401 when the Authorization header is missing.
        """
        response = await client.post("/validate_user")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    @patch("main.jwt.decode", side_effect=Exception("invalid token"))
    async def test_validate_user_invalid_token(self, jwt_decode_mock, client, valid_token):
        """
        Should return 401 for invalid token decoding.
        """
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = await client.post("/validate_user", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    @patch("main.get_user", new_callable=AsyncMock)
    @patch("main.jwt.decode")
    async def test_validate_user_user_not_found(self, jwt_decode_mock, get_user_mock, client, valid_token):
        """
        Should return 401 if the token is valid but user not found in DB.
        """
        jwt_decode_mock.return_value = {"sub": "nonexistent@example.com"}
        get_user_mock.return_value = None
        headers = {"Authorization": f"Bearer {valid_token}"}

        response = await client.post("/validate_user", headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    # === /token ===
    @patch("main.authenticate_user", new_callable=AsyncMock)
    @patch("main.create_access_token_from_email")
    async def test_login_success(self, mock_token, mock_authenticate_user, client):
        """
        Should return 200 and a token cookie on valid login.
        """
        mock_authenticate_user.return_value = MagicMock()
        mock_token.return_value = MagicMock(access_token="mocked.jwt.token")
        response = await client.post("/token", data={"username": "user@example.com", "password": "password"})

        assert response.status_code == 200
        assert response.cookies["token"] == "mocked.jwt.token"

    @patch("main.authenticate_user", new_callable=AsyncMock)
    async def test_login_failure(self, mock_authenticate_user, client):
        """
        Should return 401 on failed login credentials.
        """
        mock_authenticate_user.return_value = None
        response = await client.post("/token", data={"username": "wrong@example.com", "password": "wrong"})

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

    # === /logout ===
    async def test_logout(self, client):
        """
        Should return 200 and set Max-Age=0 to invalidate token cookie.
        """
        response = await client.post("/logout")
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out"
        assert "Max-Age=0" in response.headers.get("set-cookie", "")

    # === /sign_up ===
    @patch("main.create_new_user", new_callable=AsyncMock)
    @patch("main.create_access_token_from_email")
    async def test_sign_up_success(self, mock_token, mock_create_user, client):
        """
        Should return 200 with token cookie for valid sign-up.
        """
        mock_token.return_value = MagicMock(access_token="signed.jwt.token")
        payload = {"email": "new@user.com", "password": "pass123", "role": "student"}

        response = await client.post("/sign_up", json=payload)
        assert response.status_code == 200
        assert response.cookies["token"] == "signed.jwt.token"

    async def test_sign_up_missing_fields(self, client):
        """
        Should return 400 if any required sign-up field is missing.
        """
        payload = {"email": "", "password": "pass", "role": "student"}
        response = await client.post("/sign_up", json=payload)
        assert response.status_code == 400
        assert "required" in response.json()["detail"]

    async def test_sign_up_invalid_role(self, client):
        """
        Should return 400 for invalid role values.
        """
        payload = {"email": "x@x.com", "password": "pass", "role": "admin"}
        response = await client.post("/sign_up", json=payload)
        assert response.status_code == 400
        assert "must be student or faculty" in response.json()["detail"]

    @patch("main.create_new_user", new_callable=AsyncMock, side_effect=UserAlreadyExistsException())
    async def test_sign_up_duplicate_email(self, mock_create, client):
        """
        Should return 400 if email already exists in DB.
        """
        payload = {"email": "x@x.com", "password": "pass", "role": "student"}
        response = await client.post("/sign_up", json=payload)
        assert response.status_code == 400
        assert "already in use" in response.json()["detail"]

    def test_create_serializable_note(self):
        """
        Unit test for converting a Note object to a serializable dict.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="application/pdf", content=b"abc123")
        result = create_serializable_note(note)
        assert result["id"] == 1
        assert isinstance(result["content"], str)

    def test_create_serializable_notes(self):
        """
        Unit test for serializing a list of Note objects.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="application/pdf", content=b"abc123")
        result = create_serializable_notes([note])
        assert isinstance(result, list)
        assert result[0]["id"] == 1

    # === get_serializable_notes_for_department_and_course_strings ===
    @patch("main.get_notes_for_course_from_db", new_callable=AsyncMock)
    async def test_get_serializable_notes_success(self, mock_get_notes, client):
        """
        Tests successful serialization of notes retrieved by department and course.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="text/plain", content=b"test")
        mock_get_notes.return_value = [note]

        response = await get_serializable_notes_for_department_and_course_strings("CS", "101", False)

        content = json.loads(response.body.decode())
        assert "notes" in content
        assert isinstance(content["notes"], list)

    @patch("main.get_notes_for_course_from_db", new_callable=AsyncMock, side_effect=DepartmentDoesNotExistException())
    async def test_get_notes_department_fail(self, mock_get_notes, client):
        """
        Tests error handling when the department does not exist.
        """
        with pytest.raises(Exception) as exc:
            await get_serializable_notes_for_department_and_course_strings("XX", "101", False)
        assert "department does not exist" in str(exc.value)

    @patch("main.get_notes_for_course_from_db", new_callable=AsyncMock, side_effect=CourseDoesNotExistException())
    async def test_get_notes_course_fail(self, mock_get_notes, client):
        """
        Tests error handling when the course does not exist.
        """
        with pytest.raises(Exception) as exc:
            await get_serializable_notes_for_department_and_course_strings("CS", "BAD", False)
        assert "course does not exist" in str(exc.value)

    @patch("main.get_notes_for_course_from_db", new_callable=AsyncMock)
    async def test_get_notes_for_course_endpoint(self, mock_get_notes, client):
        """
        Tests the /get_notes_for_course endpoint for valid input.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="application/pdf", content=b"x")
        mock_get_notes.return_value = [note]
        payload = {"department": "CSDS", "course": "493", "ids_only": False}

        response = await client.post("/get_notes_for_course", json=payload)
        assert response.status_code == 200
        assert "notes" in json.loads(response.content)

    @patch("main.get_notes_for_course_from_db", new_callable=AsyncMock)
    async def test_get_notes_for_dept_course_string_split(self, mock_get_notes, client):
        """
        Tests /get_notes_for_department_and_course_string with space-separated format.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="text/plain", content=b"x")
        mock_get_notes.return_value = [note]
        payload = {"department_and_course": "CSDS 493", "ids_only": False}

        response = await client.post("/get_notes_for_department_and_course_string", json=payload)
        assert response.status_code == 200
        assert "notes" in json.loads(response.content)

    @patch("main.get_notes_for_course_from_db", new_callable=AsyncMock)
    async def test_get_notes_for_dept_course_string_concat(self, mock_get_notes, client):
        """
        Tests /get_notes_for_department_and_course_string with concatenated department and course.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="text/plain", content=b"x")
        mock_get_notes.return_value = [note]
        payload = {"department_and_course": "CSDS493", "ids_only": True}

        response = await client.post("/get_notes_for_department_and_course_string", json=payload)
        assert response.status_code == 200
        assert "notes" in json.loads(response.content)

    async def test_get_notes_for_dept_course_string_invalid_format(self, client):
        """
        Tests error handling for invalid department and course string format.
        """
        payload = {"department_and_course": "BAD", "ids_only": True}
        response = await client.post("/get_notes_for_department_and_course_string", json=payload)
        assert response.status_code == 400
        assert "formatted incorrectly" in response.json()["detail"]

    @patch("main.get_department_codes", new_callable=AsyncMock)
    async def test_get_departments(self, mock_get_departments, client):
        """
        Test retrieving all department codes.
        Ensures correct response structure and content.
        """
        mock_get_departments.return_value = ["CSDS", "MATH"]
        response = await client.get("/get_departments")
        assert response.status_code == 200
        content = json.loads(response.content)
        assert content["data"]["departments"] == ["CSDS", "MATH"]

    @patch("main.get_courses_for_department", new_callable=AsyncMock)
    async def test_get_courses_success(self, mock_get_courses, client):
        """
        Test retrieving all courses for a valid department.
        """
        mock_get_courses.return_value = ["493", "294"]
        response = await client.post("/get_courses", json={"department": "CSDS"})
        assert response.status_code == 200
        assert "courses" in json.loads(response.content)["data"]

    @patch("main.get_courses_for_department", new_callable=AsyncMock, side_effect=DepartmentDoesNotExistException())
    async def test_get_courses_department_invalid(self, mock_get_courses, client):
        """
        Test retrieving courses for an invalid department (should raise 400).
        """
        response = await client.post("/get_courses", json={"department": "BAD"})
        assert response.status_code == 400
        assert "department does not exist" in response.json()["detail"]

    @patch("main.get_sections_for_course", new_callable=AsyncMock)
    async def test_get_sections_success(self, mock_get_sections, client):
        """
        Test retrieving sections for a valid course in a valid department.
        """
        mock_get_sections.return_value = [
            SimpleNamespace(section_id=1, instructor="prof", year=2025, semester="fall")
        ]
        response = await client.post("/get_sections", json={"department": "CSDS", "course": "493"})
        assert response.status_code == 200
        content = json.loads(response.content)
        assert "sections" in content["data"]

    @patch("main.get_sections_for_course", new_callable=AsyncMock, side_effect=DepartmentDoesNotExistException())
    async def test_get_sections_department_invalid(self, mock_get_sections, client):
        """
        Test retrieving sections for an invalid department.
        """
        response = await client.post("/get_sections", json={"department": "BAD", "course": "493"})
        assert response.status_code == 400
        assert "department does not exist" in response.json()["detail"]

    @patch("main.get_sections_for_course", new_callable=AsyncMock, side_effect=CourseDoesNotExistException())
    async def test_get_sections_course_invalid(self, mock_get_sections, client):
        """
        Test retrieving sections for an invalid course.
        """
        response = await client.post("/get_sections", json={"department": "CSDS", "course": "INVALID"})
        assert response.status_code == 400
        assert "course does not exist" in response.json()["detail"]

    @patch("main.get_notes_for_section_from_db", new_callable=AsyncMock)
    async def test_get_notes_for_section_success(self, mock_get_notes, client):
        """
        Test successful retrieval of notes for a given section.
        """
        note = Note(note_id=1, section_id=2, owner_id=3, content_type="text/plain", content=b"test")
        mock_get_notes.return_value = [note]
        payload = {"section_id": 123, "ids_only": False}
        response = await client.post("/get_notes_for_section", json=payload)
        assert response.status_code == 200
        assert "notes" in json.loads(response.content)

    @patch("main.get_notes_for_section_from_db", new_callable=AsyncMock, side_effect=SectionDoesNotExistException())
    async def test_get_notes_for_section_invalid(self, mock_get_notes, client):
        """
        Test retrieval of notes for an invalid section (should raise 400).
        """
        response = await client.post("/get_notes_for_section", json={"section_id": 999, "ids_only": False})
        assert response.status_code == 400
        assert "section does not exist" in response.json()["detail"]

    @patch("main.get_notes_for_user", new_callable=AsyncMock)
    async def test_get_my_notes_success(self, mock_get_notes, client):
        """
        Test retrieval of notes uploaded by the current user.
        """
        mock_get_notes.return_value = [
            Note(note_id=1, section_id=2, owner_id=3, content_type="application/pdf", content=b"abc")
        ]
        response = await client.post("/get_my_notes", json={"ids_only": False})
        assert response.status_code == 200
        assert "notes" in json.loads(response.content)

    @patch("main.set_or_update_note_rating", new_callable=AsyncMock)
    async def test_rate_note_success(self, mock_set_rating, client):
        """
        Test successfully submitting a rating for a note.
        """
        payload = {"note_id": 1, "rating": 8}
        response = await client.post("/rate_note", json=payload)
        assert response.status_code in [200, 204]

    async def test_rate_note_invalid_rating(self, client):
        """
        Test submitting an invalid rating outside 1–10.
        """
        payload = {"note_id": 1, "rating": 0}
        response = await client.post("/rate_note", json=payload)
        assert response.status_code == 400
        assert "rating must be" in response.json()["detail"]

    @patch("main.set_or_update_note_rating", new_callable=AsyncMock, side_effect=NoteDoesNotExistException())
    async def test_rate_note_invalid_note(self, mock_set_rating, client):
        """
        Test rating a non-existent note (should raise 400).
        """
        payload = {"note_id": 999, "rating": 5}
        response = await client.post("/rate_note", json=payload)
        assert response.status_code == 400
        assert "note does not exist" in response.json()["detail"]

    @patch("main.get_average_note_rating_from_db", new_callable=AsyncMock)
    async def test_get_average_rating_success(self, mock_avg, client):
        """
        Test fetching average rating for a note.
        """
        mock_avg.return_value = 8.5
        response = await client.post("/get_average_note_rating", json={"note_id": 1})
        assert response.status_code == 200
        assert json.loads(response.content)["average_rating"] == 8.5

    @patch("main.get_average_note_rating_from_db", new_callable=AsyncMock, side_effect=NoteDoesNotExistException())
    async def test_get_average_rating_invalid(self, mock_avg, client):
        """
        Test fetching average rating for an invalid note.
        """
        response = await client.post("/get_average_note_rating", json={"note_id": 999})
        assert response.status_code == 400
        assert "note does not exist" in response.json()["detail"]

    @patch("main.leave_comment_on_note", new_callable=AsyncMock)
    async def test_leave_comment_success(self, mock_leave_comment, client):
        """
        Test successfully leaving a comment on a note.
        """
        mock_leave_comment.return_value = 99
        response = await client.post("/leave_comment", json={
            "note_id": 1, "parent_com_id": None, "content": "Great note!"
        })
        assert response.status_code == 200
        assert json.loads(response.content)["id"] == 99

    @patch("main.leave_comment_on_note", new_callable=AsyncMock, side_effect=NoteDoesNotExistException())
    async def test_leave_comment_note_invalid(self, mock_leave_comment, client):
        """
        Test commenting on a non-existent note (should raise 400).
        """
        response = await client.post("/leave_comment", json={
            "note_id": 999, "parent_com_id": None, "content": "Comment"
        })
        assert response.status_code == 400
        assert "note does not exist" in response.json()["detail"]

    @patch("main.leave_comment_on_note", new_callable=AsyncMock, side_effect=ParentCommentDoesNotExistException())
    async def test_leave_comment_parent_invalid(self, mock_leave_comment, client):
        """
        Test replying to a non-existent parent comment (should raise 400).
        """
        response = await client.post("/leave_comment", json={
            "note_id": 1, "parent_com_id": 9999, "content": "Reply!"
        })
        assert response.status_code == 400
        assert "parent comment does not exist" in response.json()["detail"]

    @patch("main.get_comments_for_note_from_db", new_callable=AsyncMock)
    async def test_get_comments_for_note_success(self, mock_get_comments, client):
        """
        Test successfully retrieving comments for a note.
        """
        comment = SimpleNamespace(
            comment_id=1, note_id=1, parent_comment_id=None,
            commenter_id="test@example.com", content="Nice"
        )
        mock_get_comments.return_value = [comment]
        response = await client.post("/get_comments_for_note", json={"note_id": 1})
        assert response.status_code == 200
        assert "comments" in json.loads(response.content)

    @patch("main.get_comments_for_note_from_db", new_callable=AsyncMock, side_effect=NoteDoesNotExistException())
    async def test_get_comments_for_note_invalid(self, mock_get_comments, client):
        """
        Test retrieving comments for an invalid note.
        """
        response = await client.post("/get_comments_for_note", json={"note_id": 999})
        assert response.status_code == 400
        assert "note does not exist" in response.json()["detail"]

    @patch("main.get_top_keyphrases_from_note_comments", new_callable=AsyncMock)
    async def test_get_comment_summary_success(self, mock_keyphrases, client):
        """
        Test extracting key phrases from note comments.
        """
        mock_keyphrases.return_value = ["well explained", "detailed"]
        response = await client.post("/get_comment_summary", json={"note_id": 1})
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["data"] == ["well explained", "detailed"]

    @patch("main.get_role_given_email_from_db", new_callable=AsyncMock)
    async def test_get_role_given_email_success(self, mock_get_role, client):
        """
        Test retrieving a user's role by email.
        """
        mock_get_role.return_value = "student"
        response = await client.post("/get_role_given_email", json={"email": "test@example.com"})
        assert response.status_code == 200
        assert json.loads(response.content)["role"] == "student"

    @patch("main.get_role_given_email_from_db", new_callable=AsyncMock, side_effect=UserDoesNotExistException())
    async def test_get_role_given_email_not_found(self, mock_get_role, client):
        """
        Test retrieving role for a non-existent email.
        """
        response = await client.post("/get_role_given_email", json={"email": "notfound@example.com"})
        assert response.status_code == 400
        assert "user does not exist" in response.json()["detail"]

    @patch("main.get_role_given_user_id_from_db", new_callable=AsyncMock)
    async def test_get_role_given_user_id_success(self, mock_get_role, client):
        """
        Test retrieving a user's role by user ID.
        """
        mock_get_role.return_value = "faculty"
        response = await client.post("/get_role_given_user_id", json={"user_id": 42})
        assert response.status_code == 200
        assert json.loads(response.content)["role"] == "faculty"

    @patch("main.get_role_given_user_id_from_db", new_callable=AsyncMock, side_effect=UserDoesNotExistException())
    async def test_get_role_given_user_id_not_found(self, mock_get_role, client):
        """
        Test retrieving role for a non-existent user ID.
        """
        response = await client.post("/get_role_given_user_id", json={"user_id": 999})
        assert response.status_code == 400
        assert "user does not exist" in response.json()["detail"]
