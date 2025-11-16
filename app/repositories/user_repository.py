from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User
from app.schemas.user_schema import UserCreate, UserUpdate


class UserRepository:

    async def get_by_id(self, session: AsyncSession, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_filter(
        self, session: AsyncSession, count: int, page: int, **kwargs
    ) -> List[User]:
        stmt = select(User)
        
        if "username" in kwargs and kwargs["username"]:
            stmt = stmt.where(User.username.ilike(f"%{kwargs['username']}%"))
        if "email" in kwargs and kwargs["email"]:
            stmt = stmt.where(User.email.ilike(f"%{kwargs['email']}%"))
        
        offset = (page - 1) * count
        stmt = stmt.offset(offset).limit(count)
        
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def count(self, session: AsyncSession, **kwargs) -> int:
        from sqlalchemy import func
        stmt = select(func.count(User.id))
        
        if "username" in kwargs and kwargs["username"]:
            stmt = stmt.where(User.username.ilike(f"%{kwargs['username']}%"))
        if "email" in kwargs and kwargs["email"]:
            stmt = stmt.where(User.email.ilike(f"%{kwargs['email']}%"))
        
        result = await session.execute(stmt)
        return result.scalar() or 0

    async def create(self, session: AsyncSession, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            description=user_data.description
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user

    async def update(
        self, session: AsyncSession, user_id: UUID, user_data: UserUpdate
    ) -> User:
        user = await self.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        update_data = user_data.model_dump(exclude_unset=True)
        if update_data:
            for key, value in update_data.items():
                setattr(user, key, value)
            await session.flush()
            await session.refresh(user)
        
        return user

    async def delete(self, session: AsyncSession, user_id: UUID) -> None:
        user = await self.get_by_id(session, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        await session.delete(user)
        await session.flush()

