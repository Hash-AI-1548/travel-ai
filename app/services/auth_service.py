from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.passport import TravelPassport
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email.lower()).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def register_user(db: Session, user_in: UserRegister) -> User:
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
    
    hashed_pwd = hash_password(user_in.password)
    user = User(
        email=user_in.email.lower(),
        hashed_password=hashed_pwd,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize empty Travel Passport for user
    passport = TravelPassport(
        user_id=user.id,
        full_name=user_in.full_name,
        languages_spoken=["English"],
        travel_styles=[],
        dietary_standards=[],
        pack_styles=[],
        current_step=1,
        is_completed=False,
        completion_percentage=10 if user_in.full_name else 0
    )
    db.add(passport)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
