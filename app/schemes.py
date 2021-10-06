from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, validator

from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES


class User(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime
    salt: str
    hashed_password: str


class SetPasswordMixin(BaseModel):
    password1: str
    password2: str

    @validator('password1')
    def password_len(cls, v, values, **kwargs):
        if len(v) < 8:
            raise ValueError('password length must be > 8')
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


class UserUpdateIn(SetPasswordMixin):
    full_name: str


class UserCreateRequest(SetPasswordMixin):
    username: str
    full_name: str

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('username must be alphanumeric')
        return v


class UserOut(BaseModel):
    pk: int
    username: str
    full_name: Optional[str]
    created_at: datetime


class UserIn(BaseModel):
    username: str
    password: str


class UserPassword(BaseModel):
    hashed_password: str
    salt: str


class TaskCreateRequest(BaseModel):
    title: str
    description: str
    user_id: int
    deadline: datetime


class JWTMeta(BaseModel):
    iat: datetime = datetime.utcnow()
    exp: datetime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    sub: str
    scope: str = 'access_token'


class JWTCredentials(BaseModel):
    pass


class JWTPayload(JWTMeta, JWTCredentials):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
