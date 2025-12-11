from fastapi.testclient import TestClient
from app.main import app
import uuid


client = TestClient(app)


def test_signup_creates_user():
    # Use a unique email to avoid collisions with existing fixtures
    email = f"pytest_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"name": "pytest user", "email": email, "password": "secret123"}
    resp = client.post("/api/auth/signup", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data.get("email") == email
    assert "id" in data
