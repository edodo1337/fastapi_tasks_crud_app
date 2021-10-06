from __future__ import annotations

from abc import ABC
from dataclasses import asdict
from typing import Any, Optional

from databases.core import Database


class BaseDAO(ABC):
    query_mapping = {'create': None, 'update': None, 'delete': None, 'get_by_id': None}
    detail_dto_class = None

    def __init__(self, *, db: Database):
        self.db = db

    async def delete(self, *, pk: int) -> int | None:
        query = self.query_mapping['delete']
        values = {'id': pk}
        return await self.db.execute(query=query, values=values)

    async def create(self, *, data: Any) -> Any:
        query = self.query_mapping['create']
        data = await self.db.execute(query=query, values=asdict(data))
        return data

    async def get_by_id(self, *, pk: int) -> Optional[Any]:
        query = self.query_mapping['get_by_id']
        values = {'id': id}
        data = await self.db.fetch_one(query=query, values=values)
        if data is None:
            return None

        return self.detail_dto_class(**data)

    async def update(self, *, data: Any) -> int | None:
        query = self.query_mapping['update']
        return await self.db.execute(query=query, values=asdict(data))
