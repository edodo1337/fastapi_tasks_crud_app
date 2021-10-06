from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Path
from fastapi.params import Depends
from starlette.responses import JSONResponse, Response

from app.schemes import UserCreateRequest, UserOut, UserUpdateIn
from app.services.auth import AuthService
from app.dependencies import get_data_access_object, get_auth_service
from app.dao.user import UserDAO, UserUniqueException
from app.logic.interactors.application import (
    user__create,
    user__delete,
    user__get_by_id,
    user__update,
)

user_router = APIRouter(prefix='/users')


@user_router.post('/')
async def user_create(
    user_in: UserCreateRequest,
    user_dao: UserDAO = Depends(get_data_access_object(UserDAO)),
    auth_service: AuthService = Depends(get_auth_service()),
) -> JSONResponse:
    try:
        await user__create(request_data=user_in, auth_service=auth_service, user_dao=user_dao)
    except UserUniqueException:
        raise HTTPException(status_code=400, detail='Username is already taken.')
    return JSONResponse({'status': 'ok'}, status_code=201)


@user_router.delete('/{user_id}')
async def user_delete(
    user_id: int = Path(..., title='User ID'),
    user_dao: UserDAO = Depends(get_data_access_object(UserDAO)),
) -> JSONResponse:
    user_id = await user__delete(user_id=user_id, user_dao=user_dao)
    if not user_id:
        return Response(status_code=204)
    return JSONResponse({'status': 'ok'}, status_code=200)


@user_router.get('/{user_id}')
async def user_detail(
    user_id: int = Path(..., title='User ID'),
    user_dao: UserDAO = Depends(get_data_access_object(UserDAO)),
) -> JSONResponse:
    user_data = await user__get_by_id(user_id=user_id, user_dao=user_dao)

    if not user_data:
        return JSONResponse(status_code=404)

    resposne_data = UserOut(
        pk=user_data.pk,
        username=user_data.username,
        full_name=user_data.full_name,
        created_at=user_data.created_at,
    )
    return JSONResponse(jsonable_encoder(resposne_data), status_code=200)


@user_router.patch('/{user_id}')
async def user_update(
    user_in: UserUpdateIn,
    user_id: int = Path(..., title='User ID'),
    user_dao: UserDAO = Depends(get_data_access_object(UserDAO)),
    auth_service: AuthService = Depends(get_auth_service()),
) -> JSONResponse:
    user_id = await user__update(
        user_id=user_id, request_data=user_in, auth_service=auth_service, user_dao=user_dao
    )
    if not user_id:
        return JSONResponse({}, status_code=404)
    return JSONResponse({'status': 'ok'}, status_code=201)
