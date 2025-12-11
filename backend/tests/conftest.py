from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import pytest
from app.database import Base, get_db
from fastapi.testclient import TestClient


# Allow CI to provide a TEST_DATABASE_URL (e.g. postgres) via env. If not set,
# fall back to a local temporary SQLite file which works reliably for TestClient.
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL") or "sqlite:///./test_temp.db"

# For SQLite we need the special connect_args; for other DBs (Postgres) we don't.
connect_args = {"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(TEST_DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    # Ensure model modules are imported so metadata includes all tables
    # (imports are idempotent)
    import app.models.user  # noqa: F401
    import app.models.project  # noqa: F401
    import app.models.project_member  # noqa: F401
    import app.models.issue  # noqa: F401
    import app.models.comment  # noqa: F401

    # Create tables
    # Point the application's database engine/session to the test engine
    import app.database as _app_db
    _app_db.engine = engine
    _app_db.SessionLocal = TestingSessionLocal

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    # Import app after test DB is prepared and dependency override is defined
    from app.main import app as _app

    # Override the dependency on the app instance
    _app.dependency_overrides[get_db] = override_get_db

    with TestClient(_app) as client:
        yield client
