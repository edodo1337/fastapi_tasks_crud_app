from __future__ import annotations

import functools
import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
SECRET = os.getenv('SECRET', 'dsakdjakdjka123')

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
DEBUG = os.getenv('DEBUG')

DATABASE_URL = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)


class Settings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = ''

    debug: bool = DEBUG
    project_name: str = 'FastAPI auth'
    project_url: str = 'http://0.0.0.0:5000'
    project_prefix_api_url: str = ''
    base_timeout: float = 60.0
    docs_url: Optional[str] = '/docs'

    app_version: str = '0.1.0'
    app_label: str = 'undefined'
    log_level: str = 'INFO'


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
