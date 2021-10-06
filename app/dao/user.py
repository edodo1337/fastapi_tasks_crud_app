from __future__ import annotations

from app.dao.base import BaseDAO
from app.dto import UserCreateDTO, UserDTO, UserUpdateDTO


class UserUniqueException(Exception):
    pass


class UserDAO(BaseDAO):
    query_mapping = {
        'create': (
            'INSERT INTO users(username, full_name, salt, hashed_password) '
            'VALUES (:username, :full_name, :salt, :hashed_password) RETURNING id'
        ),
        'delete': 'DELETE FROM users WHERE id = :id RETURNING id',
        'get_by_id': (
            'SELECT id as pk, username, created_at, full_name, hashed_password, salt '
            'FROM users WHERE id = :id LIMIT 1'
        ),
        'update': (
            'UPDATE users SET hashed_password = :hashed_password, salt = :salt, full_name = :full_name '
            'WHERE id = :id RETURNING id'
        ),
    }
    detail_dto_class = UserDTO

    async def create(self, *, data: UserCreateDTO) -> int:
        return super().create(data=data)

    async def delete(self, *, pk: int) -> int | None:
        return super().delete(pk=pk)

    async def get_by_id(self, *, pk: int) -> UserDTO | None:
        return super().get_by_id(pk=pk)

    async def update(self, *, data: UserUpdateDTO) -> int | None:
        return super().update(data=data)
