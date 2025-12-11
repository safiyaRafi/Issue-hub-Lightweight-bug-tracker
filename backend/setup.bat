@echo off
echo ========================================
echo IssueHub Backend - Simple Setup
echo ========================================
echo.

REM Create .env file
echo Creating .env file...
(
echo DATABASE_URL=sqlite:///./issuehub.db
echo SECRET_KEY=super-secret-key-change-this-in-production-abc123xyz789
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo CORS_ORIGINS=http://localhost:5173
) > .env
echo .env file created!
echo.

REM Install dependencies globally (no venv needed for quick start)
echo Installing Python dependencies...
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 sqlalchemy==2.0.23 alembic==1.12.1 pydantic==2.5.0 pydantic-settings==2.1.0 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 python-multipart==0.0.6
echo.

REM Run migrations
echo Setting up database...
alembic upgrade head
echo.

REM Seed demo data
echo Adding demo data...
python app/seed.py
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend server, run:
echo   uvicorn app.main:app --reload
echo.
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
pause
