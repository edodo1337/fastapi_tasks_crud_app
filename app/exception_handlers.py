from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
