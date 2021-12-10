from fastapi.routing import APIRouter
from fastapi.param_functions import Depends
from fastapi import Depends, FastAPI, HTTPException, status, Request
from starlette.responses import RedirectResponse

from api.user_management.dtos.login_user_dto import LoginUserDTO
from config import default_log
from data.dbapi.user_management import read_queries
from data.models.users import Users
from logic.auth.password_reset_utilities import send_reset_password_email, \
    validate_email_token, get_email_from_reset_password_request
from logic.auth.token_cache import TokenCache
from logic.auth.token_management import authenticate_user, create_access_token, \
    get_user_from_token
import config

auth_router = APIRouter(prefix='/auth', tags=['auth'])

#TODO: Use FastAPI-Users library
@auth_router.post('/login')
def login(login_user: LoginUserDTO):
    user = authenticate_user(login_user.email, login_user.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(email=user.email)

    return dict(token=access_token)


@auth_router.get('/logout')
def logout(user: Users = Depends(get_user_from_token)):
    token_cache = TokenCache()

    token_cache.delete_tokens_for_user(user.email)

    return dict(response="ok")


@auth_router.get('/reset-password/{token}')
def reset_password(token):
    return dict(response='TODO: Implement Reset password form')


@auth_router.get('/reset-password-request')
def reset_password_request(request: Request, user: Users = Depends(get_user_from_token)):
    send_reset_password_email(user.email, user)
    return dict(response="ok")



@auth_router.get('/process-reset-password-request')
def process_reset_password_request(email_token, hashed_one_time_password):
    email = get_email_from_reset_password_request(email_token, hashed_one_time_password)
    if email:
        new_jwt_token = create_access_token(email)
        return RedirectResponse(f"{config.frontend_url}/auth/reset-password/{new_jwt_token}")

    return dict(response="ok")


