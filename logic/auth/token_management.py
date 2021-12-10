from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.param_functions import Depends
from jose import jwt
from jose.exceptions import JWTError

import config
from datetime import datetime
from data.dbapi.user_management import read_queries
from data.models.users import Users
from fastapi import Depends, FastAPI, HTTPException, status

from logic.auth.redis_token_cache import RedisTokenCache
from logic.auth.token_cache import TokenCache

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Used to get jwt token from headers


def authenticate_user(email, password):
    user = read_queries.find_by_email(email)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


def create_access_token(email):
    issue_time = datetime.utcnow()
    issue_time_delta = (issue_time - datetime(1970, 1, 1)).total_seconds()
    issue_time_seconds = int(issue_time_delta)

    data_to_encode = {
        'sub': email,
        'iat': issue_time_seconds,
        'exp': datetime.now() + config.get_expiration_duration()
    }

    encoded_jwt = jwt.encode(
        data_to_encode, config.secret_key, algorithm="HS256")

    token_cache = RedisTokenCache()
    token_cache.add_token(f"{email}_{issue_time_seconds}", encoded_jwt)
    return encoded_jwt


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=['HS256'])
        email = payload.get('sub')
        iat = payload.get('iat')
        if email is None:
            raise credentials_exception

        key = f"{email}_{iat}"
        token_cache = RedisTokenCache()
        if not token_cache.verify_token(key):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = read_queries.find_by_email(email)
    if user is None:
        raise credentials_exception
    return user
