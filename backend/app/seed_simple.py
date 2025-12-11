import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember, MemberRole
from app.models.issue import Issue, IssueStatus, IssuePriority
from app.models.comment import Comment

def seed_data():
    db = SessionLocal()
    
    try:
        # Pre-hashed password for "password123" to avoid bcrypt version issues
        password_hash = "$2b$12$pvmsKkC10/3mDaPzj4qVGeaLycEPLi8vGTGxTfsms0A95RIlqC4yapt"
        
        # Create users
        user1 = User(
            name="Alice Johnson",
            email="alice@example.com",
            password_hash=password_hash
        )
        user2 = User(
            name="Bob Smith",
            email="bob@example.com",
            password_hash=password_hash
        )
        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        # Create projects
        project1 = Project(
            name="IssueHub Development",
            key="ISSUE",
            description="Main development project for IssueHub bug tracker"
        )
        project2 = Project(
            name="Mobile App",
            key="MOBILE",
            description="Mobile application development"
        )
        db.add_all([project1, project2])
        db.commit()
        db.refresh(project1)
        db.refresh(project2)
        
        # Add project members
        members = [
            ProjectMember(project_id=project1.id, user_id=user1.id, role=MemberRole.MAINTAINER),
            ProjectMember(project_id=project1.id, user_id=user2.id, role=MemberRole.MEMBER),
            ProjectMember(project_id=project2.id, user_id=user2.id, role=MemberRole.MAINTAINER),
            ProjectMember(project_id=project2.id, user_id=user1.id, role=MemberRole.MEMBER),
        ]
        db.add_all(members)
        db.commit()
        
        # Create issues for project 1
        issues_p1 = [
            Issue(
                project_id=project1.id,
                title="Setup authentication system",
                description="Implement JWT-based authentication with login and signup",
                status=IssueStatus.RESOLVED,
                priority=IssuePriority.HIGH,
                reporter_id=user1.id,
                assignee_id=user1.id
            ),
            Issue(
                project_id=project1.id,
                title="Create project management UI",
                description="Build the frontend for creating and managing projects",
                status=IssueStatus.IN_PROGRESS,
                priority=IssuePriority.HIGH,
                reporter_id=user1.id,
                assignee_id=user2.id
            ),
            Issue(
                project_id=project1.id,
                title="Add issue filtering",
                description="Implement filters for status, priority, and assignee",
                status=IssueStatus.OPEN,
                priority=IssuePriority.MEDIUM,
                reporter_id=user2.id,
                assignee_id=user1.id
            ),
            Issue(
                project_id=project1.id,
                title="Implement search functionality",
                description="Add text search for issue titles and descriptions",
                status=IssueStatus.OPEN,
                priority=IssuePriority.MEDIUM,
                reporter_id=user1.id
            ),
            Issue(
                project_id=project1.id,
                title="Database performance optimization",
                description="Optimize queries for large datasets",
                status=IssueStatus.OPEN,
                priority=IssuePriority.CRITICAL,
                reporter_id=user1.id,
                assignee_id=user1.id
            ),
        ]
        
        # Create issues for project 2
        issues_p2 = [
            Issue(
                project_id=project2.id,
                title="Design mobile UI mockups",
                description="Create mockups for all main screens",
                status=IssueStatus.RESOLVED,
                priority=IssuePriority.HIGH,
                reporter_id=user2.id,
                assignee_id=user1.id
            ),
            Issue(
                project_id=project2.id,
                title="Setup React Native project",
                description="Initialize React Native project with necessary dependencies",
                status=IssueStatus.RESOLVED,
                priority=IssuePriority.HIGH,
                reporter_id=user2.id,
                assignee_id=user2.id
            ),
            Issue(
                project_id=project2.id,
                title="Implement login screen",
                description="Create login screen with form validation",
                status=IssueStatus.IN_PROGRESS,
                priority=IssuePriority.HIGH,
                reporter_id=user2.id,
                assignee_id=user1.id
            ),
        ]
        
        db.add_all(issues_p1 + issues_p2)
        db.commit()
        
        # Add some comments
        issue1 = issues_p1[0]
        issue2 = issues_p1[1]
        
        comments = [
            Comment(
                issue_id=issue1.id,
                author_id=user2.id,
                body="Great work on implementing this! The JWT tokens are working perfectly."
            ),
            Comment(
                issue_id=issue1.id,
                author_id=user1.id,
                body="Thanks! I also added refresh token support for better security."
            ),
            Comment(
                issue_id=issue2.id,
                author_id=user1.id,
                body="I've started working on the project list view. Should have it ready by tomorrow."
            ),
        ]
        
        db.add_all(comments)
        db.commit()
        
        print("✅ Seed data created successfully!")
        print("\nDemo credentials:")
        print("User 1: alice@example.com / password123")
        print("User 2: bob@example.com / password123")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
