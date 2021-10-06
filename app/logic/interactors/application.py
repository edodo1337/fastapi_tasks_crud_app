from __future__ import annotations

from app.dao.user import UserDAO, UserUniqueException

from app.dto import TaskCreateDTO, UserCreateDTO, UserDTO, UserUpdateDTO, UsersTasksCreateDTO
from app.schemes import TaskCreateRequest, UserCreateRequest, UserUpdateIn
from app.dao.tasks import TaskUniqueException, TasksDAO
from app.dao.users_tasks import UsersTaskUniqueException, UsersTasksDAO


async def user__create(*, request_data: UserCreateRequest, auth_service, user_dao: UserDAO):
    user_credentials = auth_service.create_salt_and_hashed_password(password=request_data.password1)
    user_data = UserCreateDTO(
        username=request_data.username,
        full_name=request_data.full_name,
        salt=user_credentials.salt,
        hashed_password=user_credentials.hashed_password,
    )
    try:
        await user_dao.create(data=user_data)
    except UserUniqueException as err:
        raise err


async def user__delete(*, user_id: int, user_dao: UserDAO) -> int | None:
    user_id = await user_dao.delete(pk=user_id)
    return user_id


async def user__get_by_id(*, user_id: int, user_dao: UserDAO) -> UserDTO | None:
    return await user_dao.get_by_id(id=user_id)


async def user__update(
    *, user_id: int, request_data: UserUpdateIn, auth_service, user_dao: UserDAO
) -> int | None:
    user_credentials = auth_service.create_salt_and_hashed_password(password=request_data.password1)

    user_data = UserUpdateDTO(
        id=user_id,
        full_name=request_data.full_name,
        salt=user_credentials.salt,
        hashed_password=user_credentials.hashed_password,
    )
    user_id = await user_dao.update(data=user_data)
    return user_id


async def task__create(*, request_data: TaskCreateRequest, task_dao: TasksDAO) -> id:
    task_data = TaskCreateDTO(
        title=request_data.title,
        description=request_data.description,
        deadline=request_data.deadline,
    )
    try:
        return await task_dao.create(data=task_data)
    except TaskUniqueException as err:
        raise err


async def users_tasks__create(*, user_id: int, task_id: int, users_task_dao: UsersTasksDAO) -> id:
    users_task_data = UsersTasksCreateDTO(user_id=user_id, task_id=task_id)
    try:
        return await users_task_dao.create(data=users_task_data)
    except UsersTaskUniqueException as err:
        raise err
