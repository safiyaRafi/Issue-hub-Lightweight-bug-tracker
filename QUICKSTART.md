# IssueHub Quick Start Guide

## Prerequisites
- Python 3.11+ ✓ (You have 3.12.4)
- Node.js 18+ ✓ (You have 20.14.0)
- PostgreSQL installed and running

## Backend Setup (Terminal 1)

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create .env file (copy from .env.example):
   ```bash
   copy .env.example .env
   ```
   
   Then edit .env and update:
   - DATABASE_URL with your PostgreSQL credentials
   - SECRET_KEY with a strong random string

6. Create PostgreSQL database:
   ```bash
   # Using psql:
   psql -U postgres
   CREATE DATABASE issuehub;
   \q
   
   # OR using createdb:
   createdb issuehub
   ```

7. Run database migrations:
   ```bash
   alembic upgrade head
   ```

8. Seed demo data (optional):
   ```bash
   python app/seed.py
   ```

9. Start backend server:
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Backend running at: http://localhost:8000
   API docs at: http://localhost:8000/docs

## Frontend Setup (Terminal 2 - New Window)

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```
   
   Frontend running at: http://localhost:5173

## Access the Application

Open your browser and go to: **http://localhost:5173**

### Demo Credentials (after running seed script):
- **User 1**: alice@example.com / password123
- **User 2**: bob@example.com / password123

## Troubleshooting

### Backend Issues:
- **Database connection error**: Check PostgreSQL is running and DATABASE_URL in .env is correct
- **Module not found**: Make sure virtual environment is activated and dependencies are installed
- **Migration errors**: Drop the database and recreate it, then run migrations again

### Frontend Issues:
- **Port already in use**: Change port in vite.config.js or kill the process using port 5173
- **Module not found**: Delete node_modules and package-lock.json, then run `npm install` again
- **API connection error**: Make sure backend is running on port 8000

## Quick Commands

### Backend:
```bash
# Activate venv
venv\Scripts\activate

# Start server
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v
```

### Frontend:
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features to Test

1. **Authentication**
   - Sign up with new account
   - Log in / Log out
   
2. **Project Management**
   - Create new project
   - View projects list
   
3. **Issue Tracking**
   - Create issues
   - Filter by status/priority
   - Search issues
   - Sort issues
   
4. **Collaboration**
   - Add comments
   - Update issue status
   - Assign issues to users

Enjoy using IssueHub! 🚀
