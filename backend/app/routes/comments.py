from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.issue import Issue
from ..models.comment import Comment
from ..schemas.comment import CommentCreate, CommentResponse
from ..auth.security import get_current_user
from ..auth.permissions import check_project_access

router = APIRouter(prefix="/api/issues", tags=["comments"])

@router.get("/{issue_id}/comments", response_model=List[CommentResponse])
def list_comments(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get issue and check access
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    check_project_access(db, current_user.id, issue.project_id)
    
    # Get comments
    comments = db.query(Comment).filter(Comment.issue_id == issue_id).order_by(Comment.created_at).all()
    
    # Format response
    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "issue_id": comment.issue_id,
            "author_id": comment.author_id,
            "body": comment.body,
            "created_at": comment.created_at,
            "author_name": comment.author.name
        })
    
    return result

@router.post("/{issue_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    issue_id: int,
    request: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get issue and check access
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    check_project_access(db, current_user.id, issue.project_id)
    
    # Create comment
    new_comment = Comment(
        issue_id=issue_id,
        author_id=current_user.id,
        body=request.body
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return {
        "id": new_comment.id,
        "issue_id": new_comment.issue_id,
        "author_id": new_comment.author_id,
        "body": new_comment.body,
        "created_at": new_comment.created_at,
        "author_name": current_user.name
    }
