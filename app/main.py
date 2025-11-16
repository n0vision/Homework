import os
from litestar import Litestar, Provide
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

# Настройка базы данных
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/dbname"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def provide_db_session() -> AsyncSession:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository()


async def provide_user_service(
    user_repository: UserRepository,
    db_session: AsyncSession
) -> UserService:
    return UserService(user_repository, db_session)


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

