import uuid


def test_rehash_on_login(client, monkeypatch):
    # Create user via signup
    email = f"rehash_{uuid.uuid4().hex[:8]}@example.com"
    password = "secret123"
    r = client.post("/api/auth/signup", json={"name": "Rehash User", "email": email, "password": password})
    assert r.status_code == 201

    # Capture the original hash from the DB
    from app.database import engine
    from sqlalchemy.orm import Session
    from app.models.user import User

    with Session(bind=engine) as s:
        user = s.query(User).filter(User.email == email).first()
        old_hash = user.password_hash

    # Force the security layer to report that the hash needs update.
    # The login route imported `needs_rehash` at module import time, so patch
    # both the security module and the auth route module to ensure the route
    # observes the forced behavior.
    import app.auth.security as security
    import app.routes.auth as auth_route
    monkeypatch.setattr(security, "needs_rehash", lambda h: True)
    monkeypatch.setattr(auth_route, "needs_rehash", lambda h: True)

    # Now login (this should trigger re-hash-on-login)
    rlogin = client.post("/api/auth/login", json={"email": email, "password": password})
    assert rlogin.status_code == 200, rlogin.text

    # Confirm the stored hash changed
    with Session(bind=engine) as s:
        user2 = s.query(User).filter(User.email == email).first()
        assert user2.password_hash != old_hash
