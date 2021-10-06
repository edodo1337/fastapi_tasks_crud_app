from __future__ import annotations

from fastapi.exceptions import RequestValidationError
from app.core.utils import create_start_app_handler, create_stop_app_handler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings
from app.v1.api import api_router
from app.exception_handlers import validation_exception_handler


def get_application() -> FastAPI:
    """Base app configuration."""
    settings = get_settings()
    application = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
        version=settings.app_version,
        docs_url=settings.docs_url,
    )
    application.include_router(api_router, prefix='/v1')

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(RequestValidationError, validation_exception_handler)

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    return application


APP = get_application()
