from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Path
from fastapi.params import Depends
from starlette.responses import JSONResponse, Response

from app.schemes import TaskCreateRequest, Request, UserOut, UserUpdateIn
from app.services.auth import AuthService
from app.dependencies import get_data_access_object, get_auth_service
from app.dao.user import UserDAO
from app.logic.interactors.application import (
    user__delete,
    user__get_by_id,
    user__update,
)
from dao.tasks import TasksDAO
from dao.users_tasks import UsersTasksDAO
from logic.interactors.facades import create_task_and_bind_user

task_router = APIRouter(prefix='/tasks')


@task_router.post('/')
async def task_create(
    task_in: TaskCreateRequest,
    task_dao: TasksDAO = Depends(get_data_access_object(TasksDAO)),
    users_tasks_dao: UsersTasksDAO = Depends(get_data_access_object(UsersTasksDAO)),
) -> JSONResponse:
    task_id, users_tasks_id = create_task_and_bind_user(
        task_in=task_in, task_dao=task_dao, users_tasks_dao=users_tasks_dao
    )
    # try:

    #     await user__create(request_data=user_in, auth_service=auth_service, user_dao=user_dao)
    # except UserUniqueException:
    #     raise HTTPException(status_code=400, detail='Username is already taken.')
    return JSONResponse({'status': 'ok'}, status_code=201)


@task_router.delete('/{user_id}')
async def task_delete(
    user_id: int = Path(..., title='User ID'),
    user_dao: UserDAO = Depends(get_data_access_object(UserDAO)),
) -> JSONResponse:
    user_id = await user__delete(user_id=user_id, user_dao=user_dao)
    if not user_id:
        return Response(status_code=204)
    return JSONResponse({'status': 'ok'}, status_code=200)


@task_router.get('/{user_id}')
async def task_detail(
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


@task_router.patch('/{user_id}')
async def task_update(
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
