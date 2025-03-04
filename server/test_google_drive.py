import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_file():
    with open("test.pdf", "wb") as f:  # dummy PDF file
        f.write(b"dummy content")

    login_response = client.post("/login", json={
        "email": "fj@case.edu",
        "password": "$2b$12$PFR.Vqn9o20PMDIPvVoFz.WGQKnHhyXtWtKYD8nfyhxt.cpO0.Y.a"
    })
    token = login_response.json()["access_token"]

    with open("test.pdf", "rb") as f:
        response = client.post("/upload", headers={
            "Authorization": f"Bearer {token}"
        }, files={"file": f})

    assert response.status_code == 200
    assert "file_url" in response.json()
