# 🚀 IssueHub - Complete User Guide

## ✅ Your Servers Are Running!

You should see these in your terminals:

### Terminal 1 - Backend (Port 8000)
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2 - Frontend (Port 5173)
```
VITE v5.4.21  ready in 1305 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

---

## 🌐 Step 1: Open Your Browser

Go to: **http://localhost:5173**

You should see a beautiful login page with:
- Purple/blue gradient background
- Glassmorphism effects
- "IH" logo
- "Welcome Back" heading
- Email and Password fields
- "Sign up" link at the bottom

---

## 📝 Step 2: Create Your Account

1. **Click "Sign up"** link at the bottom of the login page

2. **Fill in the signup form**:
   - **Name**: `John Doe` (or your name)
   - **Email**: `john@example.com` (use any email)
   - **Password**: `mypassword123` (at least 6 characters)
   - **Confirm Password**: `mypassword123` (must match)

3. **Click "Create Account"**

4. You'll be automatically logged in and redirected to the Projects page

---

## 📋 Step 3: Create Your First Project

You should now see the Projects Dashboard with:
- "Projects" heading
- "+ New Project" button
- Empty state message: "No projects yet"

### Create a Project:

1. **Click "+ New Project"** button

2. **Fill in the modal form**:
   - **Project Name**: `My First Project`
   - **Project Key**: `MFP` (short code, max 10 characters)
   - **Description**: `This is my first bug tracking project`

3. **Click "Create Project"**

4. You'll see your new project card appear with:
   - The project key "MFP" in a gradient badge
   - Project name "My First Project"
   - Description
   - Creation date

5. **Click on the project card** to open it

---

## 🐛 Step 4: Create Issues (Bugs/Tasks)

You're now in the Issues List page for your project.

### Example 1: Create a Critical Bug

1. **Click "+ New Issue"** button

2. **Fill in the form**:
   - **Title**: `Login page not loading on Safari`
   - **Description**: 
     ```
     Users on Safari browser cannot access the login page.
     The page shows a blank screen.
     Steps to reproduce:
     1. Open Safari
     2. Navigate to login page
     3. Page remains blank
     ```
   - **Priority**: Select `Critical`

3. **Click "Create Issue"**

### Example 2: Create a Feature Request

1. **Click "+ New Issue"** again

2. **Fill in the form**:
   - **Title**: `Add dark mode toggle`
   - **Description**: `Users want the ability to switch between light and dark themes`
   - **Priority**: Select `Medium`

3. **Click "Create Issue"**

### Example 3: Create a Low Priority Task

1. **Click "+ New Issue"** again

2. **Fill in the form**:
   - **Title**: `Update footer copyright year`
   - **Description**: `Change copyright year from 2024 to 2025`
   - **Priority**: Select `Low`

3. **Click "Create Issue"**

---

## 🔍 Step 5: Use Filtering and Search

Now you have 3 issues. Let's try the filters:

### Filter by Priority:
1. Click the **"All Priorities"** dropdown
2. Select **"Critical"**
3. You'll see only the Safari bug

### Search Issues:
1. Clear the priority filter (select "All Priorities")
2. In the **search box**, type: `dark mode`
3. You'll see only the dark mode feature request

### Sort Issues:
1. Clear the search
2. Click the **sort dropdown** (currently "Newest First")
3. Try different options:
   - **"Recently Updated"** - shows recently modified issues first
   - **"Priority"** - shows critical issues first
   - **"Status"** - groups by status

---

## 💬 Step 6: View Issue Details and Add Comments

1. **Click on any issue card** to open the detail view

2. You'll see:
   - **Left side**: Issue title, description, status/priority badges
   - **Right side**: Details panel (Reporter, Assignee, Created date, Updated date)
   - **Comments section** below the description

### Add a Comment:

1. Scroll to the **"Add a comment..."** text area

2. Type a comment, for example:
   ```
   I've started investigating this issue. 
   Will update with findings soon.
   ```

3. **Click "Add Comment"**

4. Your comment appears with:
   - Your name
   - Timestamp
   - Comment text

### Update Issue Status (if you're a maintainer):

1. On the right sidebar, find **"Actions"** section

2. Click the **"Change Status"** dropdown

3. Select a new status:
   - **Open** - Issue is new/unstarted
   - **In Progress** - Someone is working on it
   - **Resolved** - Issue is fixed
   - **Closed** - Issue is completed

4. Status updates immediately with a success message

---

## 🎨 Step 7: Create More Projects and Issues

### Create a Second Project:

1. **Click "← Back to Projects"** at the top

2. **Click "+ New Project"**

3. Create another project:
   - **Name**: `Mobile App Development`
   - **Key**: `MOBILE`
   - **Description**: `iOS and Android app development tracking`

### Add Issues to the New Project:

1. Click on the "Mobile App Development" project

2. Create some mobile-specific issues:
   - `Setup React Native environment` (High priority)
   - `Design app icon and splash screen` (Medium priority)
   - `Implement push notifications` (Low priority)

---

## 🔗 URLs You Can Access

### Frontend URLs:
- **Main App**: http://localhost:5173
- **Login Page**: http://localhost:5173/login
- **Signup Page**: http://localhost:5173/signup
- **Projects List**: http://localhost:5173/projects
- **Specific Project**: http://localhost:5173/projects/1 (replace 1 with project ID)
- **Issue Detail**: http://localhost:5173/issues/1 (replace 1 with issue ID)

### Backend URLs:
- **API Base**: http://localhost:8000
- **API Documentation** (Interactive): http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/me (requires login)

---

## 🧪 Testing the API Directly

### Visit the API Documentation:

1. Open a new browser tab

2. Go to: **http://localhost:8000/docs**

3. You'll see Swagger UI with all API endpoints:
   - **Authentication** endpoints (signup, login, logout)
   - **Projects** endpoints (create, list, add members)
   - **Issues** endpoints (CRUD, filter, search)
   - **Comments** endpoints (list, create)

### Try an API Endpoint:

1. Find **POST /api/auth/signup** in the docs

2. Click **"Try it out"**

3. Edit the request body:
   ```json
   {
     "name": "Jane Smith",
     "email": "jane@example.com",
     "password": "password123"
   }
   ```

4. Click **"Execute"**

5. You'll see the response with the created user data

---

## 🎯 What You Should See in Your Terminals

### Backend Terminal (while using the app):

When you create a project, you'll see:
```
INFO:     127.0.0.1:xxxxx - "POST /api/projects HTTP/1.1" 200 OK
```

When you create an issue:
```
INFO:     127.0.0.1:xxxxx - "POST /api/projects/1/issues HTTP/1.1" 200 OK
```

When you add a comment:
```
INFO:     127.0.0.1:xxxxx - "POST /api/issues/1/comments HTTP/1.1" 200 OK
```

### Frontend Terminal:

You'll see hot module reload messages when files change:
```
[vite] page reload src/pages/ProjectDetail.jsx
```

---

## 🎨 Features to Explore

### 1. **Status Badges**
Issues show color-coded status badges:
- 🔵 **Open** - Blue
- 🟡 **In Progress** - Yellow
- 🟢 **Resolved** - Green
- ⚪ **Closed** - Gray

### 2. **Priority Badges**
Issues show priority indicators:
- ⚪ **Low** - Gray
- 🔵 **Medium** - Blue
- 🟠 **High** - Orange
- 🔴 **Critical** - Red

### 3. **Glassmorphism Design**
Notice the beautiful frosted glass effects on:
- Cards
- Modals
- Navigation bar
- Input fields

### 4. **Smooth Animations**
Watch for:
- Fade-in effects on page load
- Slide-up animations on cards
- Hover effects on buttons and cards
- Scale transformations on project cards

---

## 🛠️ Troubleshooting

### Can't see the login page?
- Check frontend terminal shows: `Local: http://localhost:5173/`
- Make sure you're going to the correct URL
- Try refreshing the page (Ctrl+R or Cmd+R)

### Login/Signup not working?
- Check backend terminal shows: `Application startup complete`
- Make sure backend is running on port 8000
- Check browser console for errors (F12 → Console tab)

### Issues not loading?
- Make sure you're logged in
- Check that you've created a project first
- Refresh the page

---

## 🎉 You're All Set!

You now have a fully functional bug tracking system with:
- ✅ User authentication
- ✅ Project management
- ✅ Issue tracking with priorities and statuses
- ✅ Filtering and search
- ✅ Commenting system
- ✅ Beautiful, modern UI

**Enjoy tracking your bugs!** 🚀

---

## 📌 Quick Reference

**Create Account** → **Create Project** → **Add Issues** → **Filter/Search** → **Add Comments** → **Update Status**

**Frontend**: http://localhost:5173  
**Backend API**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs
