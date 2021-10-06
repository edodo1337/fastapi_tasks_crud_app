from __future__ import annotations

from app.dao.base import BaseDAO
from app.dto import TaskDTO, TaskUpdateDTO, UsersTasksCreateDTO


class UsersTaskUniqueException(Exception):
    pass


class UsersTasksDAO(BaseDAO):
    query_mapping = {
        'create': ('INSERT INTO users_tasks(user_id, task_id) ' 'VALUES (:user_id, :task_id)'),
        'delete': 'DELETE FROM tasks WHERE id = :id RETURNING id',
        'get_by_id': (
            'SELECT id as pk, title, description, deadline, created_at, '
            'FROM tasks WHERE id = :id LIMIT 1'
        ),
        'update': (
            'UPDATE tasks SET title = :title, description = :description, deadline = :deadline '
            'WHERE id = :id RETURNING id'
        ),
    }
    detail_dto_class = TaskDTO

    async def create(self, *, data: UsersTasksCreateDTO) -> int:
        return await super().create(data=data)

    async def delete(self, *, pk: int) -> int | None:
        return await super().delete(pk=pk)

    async def get_by_id(self, *, pk: int) -> TaskDTO | None:
        return await super().get_by_id(pk=pk)

    async def update(self, *, data: TaskUpdateDTO) -> int | None:
        return await super().update(data=data)
