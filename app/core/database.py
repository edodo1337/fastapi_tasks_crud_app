from __future__ import annotations

import os
import databases
from databases.core import Database
from fastapi.applications import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger

from app.settings import DATABASE_URL

database = databases.Database(DATABASE_URL)
Base = declarative_base()


async def connect_to_db(app: FastAPI) -> None:
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else DATABASE_URL
    database = Database(DB_URL, min_size=2, max_size=10)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")


