from functools import wraps

from config import default_log
from data.db.init_db import get_db
from standard_responses.dbapi_exception_response import DBApiExceptionResponse


def dbapi_exception_handler(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        db = next(get_db())
        try:
            return function(*args, **kwargs)
        except Exception as e:
            db.rollback()
            default_log.exception(e)
            return DBApiExceptionResponse(error=str(e))
    return decorated_function
