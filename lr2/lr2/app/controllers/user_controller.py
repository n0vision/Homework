from uuid import UUID
from litestar import Controller, get, post, put, delete, Provide
from litestar.params import Parameter
from litestar.exceptions import NotFoundException, ClientException

from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide("user_service")}

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: UUID = Parameter(description="ID пользователя"),
    ) -> UserResponse:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(default=10, ge=1, le=100, description="Количество записей на странице"),
        page: int = Parameter(default=1, ge=1, description="Номер страницы"),
        username: str | None = Parameter(default=None, description="Фильтр по username"),
        email: str | None = Parameter(default=None, description="Фильтр по email"),
    ) -> dict:
        filters = {}
        if username:
            filters["username"] = username
        if email:
            filters["email"] = email
        
        users = await user_service.get_by_filter(count=count, page=page, **filters)
        total_count = await user_service.count(**filters)
        
        return {
            "users": [UserResponse.model_validate(user) for user in users],
            "total": total_count,
            "page": page,
            "count": count
        }

    @post()
    async def create_user(
        self,
        user_service: UserService,
        user_data: UserCreate,
    ) -> UserResponse:
        try:
            user = await user_service.create(user_data)
            return UserResponse.model_validate(user)
        except ValueError as e:
            raise ClientException(status_code=400, detail=str(e))

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: UUID,
        user_data: UserUpdate,
    ) -> UserResponse:
        try:
            user = await user_service.update(user_id, user_data)
            return UserResponse.model_validate(user)
        except ValueError as e:
            if "not found" in str(e).lower():
                raise NotFoundException(detail=str(e))
            raise ClientException(status_code=400, detail=str(e))

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> None:
        try:
            await user_service.delete(user_id)
        except ValueError as e:
            raise NotFoundException(detail=str(e))

