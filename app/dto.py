from __future__ import annotations
from dataclasses import dataclass
import datetime


@dataclass
class UserBaseDTO:
    full_name: str
    hashed_password: str
    salt: str


@dataclass
class UserDTO(UserBaseDTO):
    pk: int
    username: str
    created_at: datetime.datetime


@dataclass
class UserCreateDTO(UserBaseDTO):
    username: str


@dataclass
class UserUpdateDTO(UserBaseDTO):
    id: int
    ...


@dataclass
class TaskBaseDTO:
    title: str
    description: str
    deadline: datetime.datetime


@dataclass
class TaskCreateDTO(TaskBaseDTO):
    ...


@dataclass
class TaskDTO(TaskBaseDTO):
    pk: int
    created_at: datetime.datetime


@dataclass
class TaskUpdateDTO(TaskBaseDTO):
    id: int
    ...


@dataclass
class UsersTasksCreateDTO:
    user_id: int
    task_id: int
