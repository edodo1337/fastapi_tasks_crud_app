from __future__ import annotations

from fastapi import APIRouter
from starlette.responses import JSONResponse

root_router = APIRouter()


@root_router.get('/', status_code=200)
async def root() -> JSONResponse:
    return {'status': 'OK'}
