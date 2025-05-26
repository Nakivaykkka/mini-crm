from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    new_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_user_by_id(db, user_id):
    user_id = UUID(str(user_id))
    if isinstance(user_id, str):
        try:
            user_id = UUID(user_id)
        except Exception as e:
            raise ValueError(f"Invalid UUID for user_id: {user_id}")
    
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:  
    user = get_user_by_email(db, email)
    if not user:  
        return None
    if not verify_password(password, user.hashed_password):
        return None  
    return user



    



