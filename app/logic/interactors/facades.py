from __future__ import annotations

import bcrypt
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app import settings
from app.schemes import JWTPayload, TaskCreateRequest, Token, UserIn, UserPassword
from dao.tasks import TaskUniqueException, TasksDAO
from dao.users_tasks import UsersTaskUniqueException, UsersTasksDAO
from logic.interactors.application import task__create, users_tasks__create


class AuthException(BaseException):
    pass


class AuthService:
    hasher = CryptContext(schemes=['bcrypt'])
    secret = settings.SECRET

    def create_salt_and_hashed_password(self, *, password: str) -> UserPassword:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=password, salt=salt)
        return UserPassword(hashed_password=hashed_password, salt=salt)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return self.hasher.hash(password + salt)

    def encode_password(self, password: str) -> str:
        return self.hasher.hash(password)

    def verify_password(self, password: str, salt: str, hashed_password: str) -> bool:
        return self.hasher.verify(password + salt, hashed_password)

    def encode_token(self, user: UserIn) -> str:
        payload = JWTPayload(scope='access_token', sub=user.username)
        return jwt.encode(payload=payload.dict(), key=self.secret, algorithm='HS256')

    def decode_token(self, token: str) -> JWTPayload:
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return JWTPayload(**payload)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    # async def authenticate(self, user_in: UserIn, user_repo: UsersRepository) -> Token:
    #     user = await user_repo.get_by_username(username=user_in.username)
    #     if not user:
    #         raise AuthException

    #     if not self.verify_password(user_in.password, user.salt, user.hashed_password):
    #         raise AuthException

    #     token = Token(access_token=self.encode_token(user), token_type='bearer')
    #     return token


def create_task_and_bind_user(
    *, task_in: TaskCreateRequest, task_dao: TasksDAO, users_tasks_dao: UsersTasksDAO
) -> tuple[int, int]:
    try:
        task_id = task__create(request_data=task_in, task_dao=task_dao)
        users_tasks_id = users_tasks__create(
            user_id=task_in.user_id, task_id=task_id, users_tasks_dao=users_tasks_dao
        )
        return task_id, users_tasks_id
    except (TaskUniqueException, UsersTaskUniqueException) as err:
        raise err
