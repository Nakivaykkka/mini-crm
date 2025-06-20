from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID


from app.user.models import User
from app.user.schemas import UserCreate
from app.security.password import hash_password


async def user_create(
    user_in: UserCreate,
    db: AsyncSession
) -> User:
    result = await db.execute(
        select(User).where(User.email == user_in.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    
    hashed_pw = hash_password(user_in.password)
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_pw,
        phone=user_in.phone,
        role=user_in.role.value
        
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(
    user_id: UUID,
    db:AsyncSession
) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_email(
    user_email:str,
    db: AsyncSession
) -> User | None:
    result = await db.execute(
        select(User).where(User.email == user_email)
    )
    return result.scalar_one_or_none()
    