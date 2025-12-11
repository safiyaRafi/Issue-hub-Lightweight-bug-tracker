from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..database import get_db
from ..models.user import User
from ..models.issue import Issue, IssueStatus, IssuePriority
from ..schemas.issue import IssueCreate, IssueUpdate, IssueResponse
from ..auth.security import get_current_user
from ..auth.permissions import check_project_access, check_maintainer_access

router = APIRouter(prefix="/api", tags=["issues"])

@router.get("/projects/{project_id}/issues", response_model=List[IssueResponse])
def list_issues(
    project_id: int,
    q: Optional[str] = Query(None, description="Search query"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    assignee: Optional[int] = Query(None, description="Filter by assignee ID"),
    sort: Optional[str] = Query("created_at", description="Sort field"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check access
    check_project_access(db, current_user.id, project_id)
    
    # Base query
    query = db.query(Issue).filter(Issue.project_id == project_id)
    
    # Apply filters
    if q:
        query = query.filter(
            or_(
                Issue.title.ilike(f"%{q}%"),
                Issue.description.ilike(f"%{q}%")
            )
        )
    
    if status:
        query = query.filter(Issue.status == status)
    
    if priority:
        query = query.filter(Issue.priority == priority)
    
    if assignee:
        query = query.filter(Issue.assignee_id == assignee)
    
    # Apply sorting
    if sort == "priority":
        query = query.order_by(Issue.priority.desc())
    elif sort == "status":
        query = query.order_by(Issue.status)
    elif sort == "updated_at":
        query = query.order_by(Issue.updated_at.desc())
    else:
        query = query.order_by(Issue.created_at.desc())
    
    issues = query.all()
    
    # Format response with user names
    result = []
    for issue in issues:
        assignee_name = None
        if issue.assignee_id:
            assignee = db.query(User).filter(User.id == issue.assignee_id).first()
            if assignee:
                assignee_name = assignee.name
        
        result.append({
            "id": issue.id,
            "project_id": issue.project_id,
            "title": issue.title,
            "description": issue.description,
            "status": issue.status.value,
            "priority": issue.priority.value,
            "reporter_id": issue.reporter_id,
            "assignee_id": issue.assignee_id,
            "created_at": issue.created_at,
            "updated_at": issue.updated_at,
            "reporter_name": issue.reporter.name,
            "assignee_name": assignee_name
        })
    
    return result

@router.post("/projects/{project_id}/issues", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
def create_issue(
    project_id: int,
    request: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check access
    check_project_access(db, current_user.id, project_id)
    
    # Validate priority
    try:
        priority = IssuePriority(request.priority)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid priority value"
        )
    
    # Create issue
    new_issue = Issue(
        project_id=project_id,
        title=request.title,
        description=request.description,
        priority=priority,
        reporter_id=current_user.id,
        assignee_id=request.assignee_id
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    
    # Get assignee name if exists
    assignee_name = None
    if new_issue.assignee_id:
        assignee = db.query(User).filter(User.id == new_issue.assignee_id).first()
        if assignee:
            assignee_name = assignee.name
    
    return {
        "id": new_issue.id,
        "project_id": new_issue.project_id,
        "title": new_issue.title,
        "description": new_issue.description,
        "status": new_issue.status.value,
        "priority": new_issue.priority.value,
        "reporter_id": new_issue.reporter_id,
        "assignee_id": new_issue.assignee_id,
        "created_at": new_issue.created_at,
        "updated_at": new_issue.updated_at,
        "reporter_name": new_issue.reporter.name,
        "assignee_name": assignee_name
    }

@router.get("/issues/{issue_id}", response_model=IssueResponse)
def get_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Check access
    check_project_access(db, current_user.id, issue.project_id)
    
    # Get assignee name if exists
    assignee_name = None
    if issue.assignee_id:
        assignee = db.query(User).filter(User.id == issue.assignee_id).first()
        if assignee:
            assignee_name = assignee.name
    
    return {
        "id": issue.id,
        "project_id": issue.project_id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status.value,
        "priority": issue.priority.value,
        "reporter_id": issue.reporter_id,
        "assignee_id": issue.assignee_id,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
        "reporter_name": issue.reporter.name,
        "assignee_name": assignee_name
    }

@router.patch("/issues/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: int,
    request: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Check if user can update (reporter can update their own, maintainer can update any)
    membership = check_project_access(db, current_user.id, issue.project_id)
    
    # Only maintainers can change status and assignee
    if (request.status or request.assignee_id is not None) and membership.role.value != "maintainer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only maintainers can change status and assignee"
        )
    
    # Update fields
    if request.title:
        issue.title = request.title
    if request.description is not None:
        issue.description = request.description
    if request.status:
        try:
            issue.status = IssueStatus(request.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status value"
            )
    if request.priority:
        try:
            issue.priority = IssuePriority(request.priority)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid priority value"
            )
    if request.assignee_id is not None:
        issue.assignee_id = request.assignee_id
    
    db.commit()
    db.refresh(issue)
    
    # Get assignee name if exists
    assignee_name = None
    if issue.assignee_id:
        assignee = db.query(User).filter(User.id == issue.assignee_id).first()
        if assignee:
            assignee_name = assignee.name
    
    return {
        "id": issue.id,
        "project_id": issue.project_id,
        "title": issue.title,
        "description": issue.description,
        "status": issue.status.value,
        "priority": issue.priority.value,
        "reporter_id": issue.reporter_id,
        "assignee_id": issue.assignee_id,
        "created_at": issue.created_at,
        "updated_at": issue.updated_at,
        "reporter_name": issue.reporter.name,
        "assignee_name": assignee_name
    }

@router.delete("/issues/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Only maintainers can delete
    check_maintainer_access(db, current_user.id, issue.project_id)
    
    db.delete(issue)
    db.commit()
    
    return None
