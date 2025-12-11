import uuid


def signup(client, name=None, email=None, password="secret123"):
    name = name or "Test User"
    email = email or f"test_{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post("/api/auth/signup", json={"name": name, "email": email, "password": password})
    return resp


def login(client, email, password="secret123"):
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    return resp


def test_duplicate_signup(client):
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
    r1 = signup(client, email=email)
    assert r1.status_code == 201
    r2 = signup(client, email=email)
    assert r2.status_code == 400


def test_login_and_project_flow(client):
    # Signup
    email = f"flow_{uuid.uuid4().hex[:8]}@example.com"
    r = signup(client, email=email)
    assert r.status_code == 201

    # Login
    rlogin = login(client, email=email)
    assert rlogin.status_code == 200
    token = rlogin.json().get("access_token")
    assert token
    headers = {"Authorization": f"Bearer {token}"}

    # Create project
    proj_payload = {"name": "Test Project", "key": f"TP{uuid.uuid4().hex[:4]}", "description": "desc"}
    rproj = client.post("/api/projects", json=proj_payload, headers=headers)
    assert rproj.status_code == 201
    proj = rproj.json()
    project_id = proj.get("id")

    # Create issue
    issue_payload = {"title": "Bug 1", "description": "An issue", "priority": "medium"}
    rissue = client.post(f"/api/projects/{project_id}/issues", json=issue_payload, headers=headers)
    assert rissue.status_code == 201
    issue = rissue.json()
    issue_id = issue.get("id")

    # Add comment
    comment_payload = {"body": "This is a comment"}
    rcomment = client.post(f"/api/issues/{issue_id}/comments", json=comment_payload, headers=headers)
    assert rcomment.status_code == 201
    c = rcomment.json()
    assert c.get("body") == "This is a comment"