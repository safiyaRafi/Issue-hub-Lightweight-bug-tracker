# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed
- Signup response serialization: Pydantic response models now read SQLAlchemy ORM objects correctly so user objects can be returned from endpoints.
- SQLite compatibility: timestamp defaults changed from SQL function `now()` to `CURRENT_TIMESTAMP` (models + Alembic migration) to avoid sqlite3 unknown function errors.

### Security
- Password hashing: switched to a portable Passlib CryptContext using `pbkdf2_sha256` for CI/dev portability. Recommend migrating to `bcrypt` or `argon2` for production environments.
- Hardened JWT handling: `sub` claim is safely cast to int before DB lookup to avoid type mismatches.

### Tests and CI
- Added integration tests for signup and end-to-end flows (projects, issues, comments).
- Test DB: tests now use a file-based temporary SQLite DB to avoid TestClient/in-memory DB connection visibility issues.
- CI: GitHub Actions updated to run a Python version matrix and a Postgres job that validates Alembic migrations against PostgreSQL.

### Frontend
- Improved signup error handling to display backend-provided error messages when available.

## How to verify locally

1. Backend

   ```bash
   python -m venv venv
   . venv/Scripts/activate
   pip install -r backend/requirements.txt
   cd backend
   alembic upgrade head
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. Run tests

   ```bash
   . venv/Scripts/activate
   python -m pytest -q
   ```

3. Signup quick check (curl)

   ```bash
   curl -i -X POST "http://127.0.0.1:8000/api/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test User","email":"test+local@example.com","password":"secret123"}'
   ```

## Next steps / Recommendations

- Replace `pbkdf2_sha256` with `bcrypt` or `argon2` in production, and provide a migration strategy for existing password hashes.
- Expand test coverage (validation edge cases, role-based permissions, rate-limiting behavior).
- Add a small `docker-compose` dev setup with Postgres for local parity with CI.
- Add linting/type checks (ruff/mypy) to CI to catch style and type issues early.

---
Generated on: 2025-12-11
