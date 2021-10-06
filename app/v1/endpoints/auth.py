# from __future__ import annotations

# from fastapi import APIRouter, HTTPException
# from fastapi.params import Depends
# from starlette.responses import JSONResponse

# from app.schemes import Token, UserCreate, UserCreateRequest, UserIn
# from app.services.auth import AuthException, AuthService
# from app.repositories.users import UserUniqueException, UsersRepository
# from app.dependencies import get_repository, get_auth_service


# auth_router = APIRouter()


# @auth_router.post('/signup')
# async def signup(
#     user_in: UserCreateRequest,
#     user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
#     auth_service: AuthService = Depends(get_auth_service()),
# ) -> JSONResponse:
#     user_credentials = auth_service.create_salt_and_hashed_password(password=user_in.password)
#     user_data = UserCreate(
#         username=user_in.username,
#         is_active=True,
#         salt=user_credentials.salt,
#         hashed_password=user_credentials.hashed_password,
#     )
#     try:
#         await user_repo.create(user_data)
#     except UserUniqueException:
#         raise HTTPException(status_code=400, detail='Username is already taken.')
#     return JSONResponse({'status': 'ok'}, status_code=201)


# @auth_router.post('/login')
# async def login(
#     user_in: UserIn,
#     user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
#     auth_service: AuthService = Depends(get_auth_service()),
# ) -> Token:
#     try:
#         return await auth_service.authenticate(user_in=user_in, user_repo=user_repo)
#     except AuthException:
#         raise HTTPException(status_code=400, detail='Login or password is not correct')


# @auth_router.get('/refresh_token')
# async def refresh_token(token: str) -> JSONResponse:
#     from app.core.database import database

#     query = 'SELECT * FROM users;'
#     rows = await database.fetch_all(query=query)
#     return rows
#     # return 'Refresh token'


# @auth_router.post('/secret')
# async def secret_data() -> JSONResponse:
#     return 'Secret data'


# @auth_router.get('/notsecret')
# async def not_secret_data() -> JSONResponse:
#     return 'Not secret data'
