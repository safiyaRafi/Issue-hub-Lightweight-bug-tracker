# 🚀 IssueHub - Super Simple Setup

## One-Time Setup (Do this first!)

### Backend Setup
1. Open Command Prompt
2. Navigate to backend folder:
   ```bash
   cd backend
   ```
3. **Double-click `SETUP.bat`** or run:
   ```bash
   SETUP.bat
   ```
   
   This will automatically:
   - Create the .env configuration file
   - Install all Python dependencies
   - Create the SQLite database
   - Run database migrations
   - Add demo data with sample users and issues

### Frontend Setup
1. Open a NEW Command Prompt window
2. Navigate to frontend folder:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application (Every time)

### Method 1: Double-Click (Easiest!)
1. **Double-click `backend\START.bat`** - Opens backend server
2. **Double-click `frontend\START.bat`** - Opens frontend server
3. Open browser to **http://localhost:5173**

### Method 2: Command Line
**Terminal 1 - Backend:**
```bash
cd backend
START.bat
```

**Terminal 2 - Frontend:**
```bash
cd frontend
START.bat
```

## 🎉 Access the Application

Open your browser and go to: **http://localhost:5173**

### Demo Login Credentials:
- **Email**: alice@example.com
- **Password**: password123

OR

- **Email**: bob@example.com
- **Password**: password123

## 📁 What You'll See

1. **Beautiful Login Page** - Glassmorphism design with gradients
2. **Projects Dashboard** - Create and manage projects
3. **Issues List** - Filter, search, and sort issues
4. **Issue Details** - View and comment on issues
5. **API Docs** - Visit http://localhost:8000/docs

## ⚡ Quick Troubleshooting

**Backend won't start?**
- Make sure you ran `SETUP.bat` first
- Check if port 8000 is already in use

**Frontend won't start?**
- Make sure you ran `npm install` first
- Check if port 5173 is already in use

**Can't login?**
- Make sure backend is running
- Make sure you ran the seed script (part of SETUP.bat)

## 🎯 That's It!

No PostgreSQL needed! No virtual environments! Just run the setup scripts and start coding!

---

**Note**: This uses SQLite for simplicity. For production, you'd want to use PostgreSQL as originally designed.
