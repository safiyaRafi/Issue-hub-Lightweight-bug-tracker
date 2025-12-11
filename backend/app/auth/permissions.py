from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.project_member import ProjectMember, MemberRole

def check_project_access(db: Session, user_id: int, project_id: int) -> ProjectMember:
    """Check if user has access to project, return membership"""
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this project"
        )
    return membership

def check_maintainer_access(db: Session, user_id: int, project_id: int) -> ProjectMember:
    """Check if user is a maintainer of the project"""
    membership = check_project_access(db, user_id, project_id)
    
    if membership.role != MemberRole.MAINTAINER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project maintainers can perform this action"
        )
    return membership
