from fastapi import (
    Depends,
    HTTPException,
    status
)
from fastapi.security import HTTPBearer
from app.security.enums import UserRole
from fastapi import Depends, HTTPException
    
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_async_session
from app.core.config import settings
from app.user.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")
bearer_scheme = HTTPBearer()

async def get_current_user(
    token_oauth: str = Depends(oauth2_scheme),
    bearer_token = Depends(bearer_scheme),
    db=Depends(get_async_session)
):
    token = None
    if bearer_token and hasattr(bearer_token, "credentials"):
        token = bearer_token.credentials
    elif token_oauth:
        token = token_oauth

    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_roles(allowed: list[UserRole]):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {', '.join(r.value for r in allowed)}"
            )
        return current_user
    return checker


require_admin = require_roles([UserRole.admin])
require_manager = require_roles([UserRole.manager])
require_superuser = require_roles([UserRole.superuser])
