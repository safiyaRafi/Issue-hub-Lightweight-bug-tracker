# Lightweight bug tracker
A modern, full-stack bug tracking application built with FastAPI and React. IssueHub enables teams to create projects, file issues, track progress, and collaborate through comments with role-based access control.

## Development quickstart

These instructions show how to run the backend, apply migrations, run tests, and start the frontend on a development machine.

Prerequisites:
- Python 3.11+ (3.12 supported)
- Node.js 18+ (for frontend)

Backend
1. Create and activate a virtual environment:

  On Windows (Git Bash):
  python -m venv venv
  . venv/Scripts/activate

2. Install Python dependencies:

  pip install --upgrade pip
  pip install -r backend/requirements.txt

3. Run migrations:

  cd backend
  alembic upgrade head

4. Start the backend (development):

  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

5. Run tests:

  From the repository root:
  . venv/Scripts/activate
  python -m pytest -q

Frontend
1. Install dependencies and run dev server:

  cd frontend
  npm install
  npm run dev

2. Open the frontend at the URL printed by Vite (usually http://localhost:5173) and it will proxy API requests to the backend if configured.

Notes
- CI: a minimal GitHub Actions workflow runs backend tests (pytest) on push/PR.
- Database: PostgreSQL is recommended for production; SQLite is used for local development and tests by default.
- Password hashing: the backend uses Passlib. For portability in CI/dev the repo falls back to PBKDF2-SHA256; prefer `bcrypt` or `argon2` in production and set `PREFERRED_PASSWORD_SCHEME` accordingly.
# IssueHub — Lightweight Bug Tracker

A modern, full-stack bug tracking application built with FastAPI and React. IssueHub enables teams to create projects, file issues, track progress, and collaborate through comments with role-based access control.

![IssueHub](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based auth with httpOnly cookies
- 👥 **Project Management** - Create projects and manage team members
- 🐛 **Issue Tracking** - Full CRUD operations with status and priority
- 🔍 **Advanced Filtering** - Search, filter by status/priority/assignee, and sort
- 💬 **Commenting System** - Threaded discussions on issues
- 🎨 **Modern UI** - Glassmorphism design with smooth animations
- 🔒 **Role-Based Access** - Member and Maintainer roles with different permissions
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework with automatic API docs
- **PostgreSQL** - Production-grade relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration management
- **JWT** - Secure token-based authentication
- **Bcrypt** - Password hashing
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client with interceptors
- **Tailwind CSS** - Utility-first CSS framework
- **Inter Font** - Clean, modern typography

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- npm or yarn

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Lightweight-bug-tracker
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and update DATABASE_URL and SECRET_KEY
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb issuehub

# Or using psql:
psql -U postgres
CREATE DATABASE issuehub;
\q

# Run migrations
alembic upgrade head

# (Optional) Seed demo data
python app/seed.py
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## 🏃 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

## 🔑 Demo Credentials

After running the seed script, you can use these credentials:

- **User 1**: alice@example.com / password123
- **User 2**: bob@example.com / password123

## 📚 API Documentation

### Authentication

#### POST /api/auth/signup
Create a new user account.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-12-11T12:00:00Z"
}
```

#### POST /api/auth/login
Authenticate and receive JWT token.

**Request:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### GET /api/me
Get current user profile (requires authentication).

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-12-11T12:00:00Z"
}
```

### Projects

#### POST /api/projects
Create a new project (creator becomes maintainer).

**Request:**
```json
{
  "name": "My Project",
  "key": "MP",
  "description": "Project description"
}
```

#### GET /api/projects
List all projects where user is a member.

#### POST /api/projects/{id}/members
Add a member to project (maintainers only).

**Request:**
```json
{
  "email": "user@example.com",
  "role": "member"
}
```

### Issues

#### GET /api/projects/{id}/issues
List issues with optional filtering and sorting.

**Query Parameters:**
- `q` - Search in title/description
- `status` - Filter by status (open, in_progress, resolved, closed)
- `priority` - Filter by priority (low, medium, high, critical)
- `assignee` - Filter by assignee ID
- `sort` - Sort by field (created_at, updated_at, priority, status)

#### POST /api/projects/{id}/issues
Create a new issue.

**Request:**
```json
{
  "title": "Bug in login",
  "description": "Users cannot log in",
  "priority": "high",
  "assignee_id": 2
}
```

#### GET /api/issues/{id}
Get issue details.

#### PATCH /api/issues/{id}
Update issue (status/assignee changes require maintainer role).

**Request:**
```json
{
  "status": "in_progress",
  "assignee_id": 3
}
```

#### DELETE /api/issues/{id}
Delete issue (maintainers only).

### Comments

#### GET /api/issues/{id}/comments
List all comments for an issue.

#### POST /api/issues/{id}/comments
Add a comment to an issue.

**Request:**
```json
{
  "body": "This is a comment"
}
```

## 🏗️ Architecture

### Backend Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API endpoints
│   ├── auth/            # Authentication & permissions
│   ├── database.py      # Database configuration
│   ├── config.py        # Settings management
│   ├── main.py          # FastAPI application
│   └── seed.py          # Demo data script
├── alembic/             # Database migrations
├── tests/               # Test suite
└── requirements.txt     # Python dependencies
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/           # Page components
│   ├── contexts/        # React contexts (Auth)
│   ├── utils/           # Utilities (API client)
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
└── package.json         # Node dependencies
```

## 🔒 Security Features

- **Password Hashing**: Passlib CryptContext with PBKDF2-SHA256 fallback; recommended to enable `bcrypt` or `argon2` in production.
- **JWT Tokens**: Returned on login and can be stored in httpOnly cookies or used as Bearer tokens in Authorization headers.
- **CORS**: Configured via `app/config.py` to allow specified frontend origins.
- **Input Validation**: Pydantic models validate all requests and responses.
- **SQL Injection Prevention**: Use of SQLAlchemy ORM avoids manual SQL concatenation.
- **Role-Based Access Control**: Member and Maintainer roles enforced by backend permissions.

## 🎨 Design Decisions

### Why FastAPI?
- Automatic API documentation (Swagger/OpenAPI)
- High performance (async support)
- Built-in data validation with Pydantic
- Modern Python features (type hints)

### Why PostgreSQL?
- Production-grade reliability
- ACID compliance
- Rich data types and indexing
- Excellent SQLAlchemy support

### Why React + Vite?
- Fast development with HMR
- Modern build tooling
- Component-based architecture
- Large ecosystem

### Why Tailwind CSS?
- Rapid UI development
- Consistent design system
- Small production bundle
- Easy customization

## ⚠️ Known Limitations

1. **Email Notifications**: Not implemented - would require SMTP configuration
2. **File Attachments**: Issues don't support file uploads
3. **Real-time Updates**: No WebSocket support for live updates
4. **Pagination**: Frontend displays all results (backend ready for pagination)
5. **Advanced Search**: No full-text search (could add PostgreSQL FTS)
6. **Audit Logs**: No tracking of who changed what
7. **Issue Dependencies**: Cannot link related issues
8. **Time Tracking**: No time estimation or tracking features

## 🚀 Future Improvements

With more time, I would add:

1. **Enhanced Features**
   - Email notifications for issue updates
   - File attachments for issues
   - Issue labels and tags
   - Custom fields per project
   - Kanban board view
   - Activity timeline
   - Issue templates

2. **Technical Improvements**
   - WebSocket for real-time updates
   - Redis caching layer
   - Full-text search with Elasticsearch
   - Rate limiting
   - API versioning
   - Comprehensive test coverage (>90%)
   - E2E tests with Playwright

3. **DevOps**
   - Docker containerization
   - CI/CD pipeline
   - Kubernetes deployment
   - Monitoring and logging (Sentry, DataDog)
   - Database backups automation

4. **UX Enhancements**
   - Keyboard shortcuts
   - Drag-and-drop issue reordering
   - Bulk operations
   - Export to CSV/PDF
   - Dark/light theme toggle
   - Mobile app (React Native)

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 👨‍💻 Author

Built with as a demonstration of full-stack development skills.

---

**Note**: This is a production-ready MVP. For deployment, ensure you:
- Use strong SECRET_KEY in production
- Enable HTTPS
- Configure proper CORS origins
- Set up database backups
- Use environment-specific configurations
- Add monitoring and logging
