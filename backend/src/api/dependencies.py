from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session
from ..core.database import get_session
from ..models.user import User
from uuid import UUID

def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    user_id = request.cookies.get("session")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )

    user = session.get(User, user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
