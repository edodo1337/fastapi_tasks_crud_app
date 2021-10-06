from __future__ import annotations


from app.dao.base import BaseDAO
from app.dto import TaskCreateDTO, TaskDTO, TaskUpdateDTO


class TaskUniqueException(Exception):
    pass


class TasksDAO(BaseDAO):
    query_mapping = {
        'create': (
            'INSERT INTO tasks(title, description, deadline) '
            'VALUES (:username, :title, :description, :deadline) RETURNING id'
        ),
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

    async def create(self, *, data: TaskCreateDTO) -> int:
        return super().create(data=data)

    async def delete(self, *, pk: int) -> int | None:
        return super().delete(pk=pk)

    async def get_by_id(self, *, pk: int) -> TaskDTO | None:
        return super().get_by_id(pk=pk)

    async def update(self, *, data: TaskUpdateDTO) -> int | None:
        return super().update(data=data)
