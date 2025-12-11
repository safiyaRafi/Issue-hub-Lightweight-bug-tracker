@echo off
echo Starting IssueHub Backend Server...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload
