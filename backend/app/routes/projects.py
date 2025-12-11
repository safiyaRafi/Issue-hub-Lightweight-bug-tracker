from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.project_member import ProjectMember, MemberRole
from ..schemas.project import ProjectCreate, ProjectResponse, AddMemberRequest, MemberResponse
from ..auth.security import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    request: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if project key already exists
    existing_project = db.query(Project).filter(Project.key == request.key).first()
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project key already exists"
        )
    
    # Create project
    new_project = Project(
        name=request.name,
        key=request.key,
        description=request.description
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    # Add creator as maintainer
    membership = ProjectMember(
        project_id=new_project.id,
        user_id=current_user.id,
        role=MemberRole.MAINTAINER
    )
    db.add(membership)
    db.commit()
    
    return new_project

@router.get("", response_model=List[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get all projects where user is a member
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()
    
    project_ids = [m.project_id for m in memberships]
    projects = db.query(Project).filter(Project.id.in_(project_ids)).all()
    
    return projects

@router.post("/{project_id}/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def add_member(
    project_id: int,
    request: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if current user is maintainer
    from ..auth.permissions import check_maintainer_access
    check_maintainer_access(db, current_user.id, project_id)
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already a member
    existing_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member"
        )
    
    # Add member
    role = MemberRole.MAINTAINER if request.role == "maintainer" else MemberRole.MEMBER
    new_member = ProjectMember(
        project_id=project_id,
        user_id=user.id,
        role=role
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    
    return {
        "id": new_member.id,
        "user_id": user.id,
        "role": new_member.role.value,
        "user_name": user.name,
        "user_email": user.email
    }
