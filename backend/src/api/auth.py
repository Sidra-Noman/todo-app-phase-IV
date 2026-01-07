from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlmodel import Session, select
from ..core.database import get_session
from ..models.user import User
from ..schemas.user import UserCreate, UserSignin, UserResponse
from ..services.auth_service import hash_password, verify_password
from .dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "Account created successfully", "user": {"id": str(new_user.id), "email": new_user.email}}

@router.post("/signin")
def signin(user_data: UserSignin, response: Response, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    user = session.exec(statement).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # In Phase II, we use a simple session-like approach with HTTP-only cookie
    # Setting the user ID as the session token for simplicity as per requirements
    response.set_cookie(
        key="session",
        value=str(user.id),
        httponly=True,
        samesite="lax",
        secure=False # Set to True in production
    )

    return {"message": "Successfully authenticated"}

@router.post("/signout")
def signout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie("session")
    return {"message": "Successfully signed out"}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "createdAt": current_user.created_at.isoformat()
        }
    }
