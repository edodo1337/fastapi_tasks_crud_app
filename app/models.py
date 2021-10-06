from __future__ import annotations

from sqlalchemy import Column, Integer
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR, Boolean

from app.core.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    username = Column(VARCHAR(length=255), unique=True, nullable=False)
    full_name = Column(VARCHAR(length=255), unique=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.NOW(), nullable=False)
    is_active = Column(Boolean, default=True, server_default='t', nullable=False)
    salt = Column(VARCHAR(length=255), nullable=False)
    hashed_password = Column(VARCHAR(length=255), nullable=False)


class UsersTasks(Base):
    __tablename__ = 'users_tasks'
    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    title = Column(VARCHAR(length=255), unique=True, nullable=False)
    description = Column(VARCHAR(length=255), unique=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.NOW(), nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=False)
