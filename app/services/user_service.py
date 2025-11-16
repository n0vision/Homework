from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from models import User


class UserService:

    def __init__(self, user_repository: UserRepository, db_session: AsyncSession):
        self.user_repository = user_repository
        self.db_session = db_session

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(self.db_session, user_id)

    async def get_by_filter(
        self, count: int, page: int, **kwargs
    ) -> List[User]:
        return await self.user_repository.get_by_filter(
            self.db_session, count, page, **kwargs
        )

    async def count(self, **kwargs) -> int:
        return await self.user_repository.count(self.db_session, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repository.get_by_filter(
            self.db_session, count=1, page=1, email=user_data.email
        )
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")
        
        existing_username = await self.user_repository.get_by_filter(
            self.db_session, count=1, page=1, username=user_data.username
        )
        if existing_username:
            raise ValueError(f"User with username {user_data.username} already exists")
        
        user = await self.user_repository.create(self.db_session, user_data)
        await self.db_session.commit()
        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        if user_data.email:
            existing_user = await self.user_repository.get_by_filter(
                self.db_session, count=1, page=1, email=user_data.email
            )
            if existing_user and existing_user[0].id != user_id:
                raise ValueError(f"User with email {user_data.email} already exists")
        
        if user_data.username:
            existing_username = await self.user_repository.get_by_filter(
                self.db_session, count=1, page=1, username=user_data.username
            )
            if existing_username and existing_username[0].id != user_id:
                raise ValueError(f"User with username {user_data.username} already exists")
        
        user = await self.user_repository.update(self.db_session, user_id, user_data)
        await self.db_session.commit()
        return user

    async def delete(self, user_id: UUID) -> None:
        await self.user_repository.delete(self.db_session, user_id)
        await self.db_session.commit()

