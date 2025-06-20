from fastapi import(
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.user.schemas import (
    UserRead,
    UserCreate,
    UserLogin
)
from app.user.service  import (
    user_create,
    get_user_by_id,
    get_user_by_email
)
from app.core.database import get_async_session
from app.security.tokens import create_access_token, create_refresh_token
from app.security.password import verify_password

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/create", response_model=UserRead, status_code=201)
async def user_create_router(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    return await user_create(user, db)

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login/")
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_async_session)
):
    user = await get_user_by_email(credentials.email, db)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
        }