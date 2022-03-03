from functools import wraps

from config import default_log
from data.db.init_db import get_db
from standard_responses.dbapi_exception_response import DBApiExceptionResponse
from fastapi import HTTPException


 
def frontend_api_generic_exception(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            default_log.exception(e)
            #TODO: Use JSONResponse
            raise HTTPException(
                status_code=400,
                detail=str(e),
            )
    return decorated_function
 
 
def dbapi_exception_handler(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        db = None
        try:
            if not kwargs.get('session'):
                kwargs['session'] = next(get_db())
            db = kwargs['session']
            retval = function(*args, **kwargs)
            if kwargs.get('commit'):
                db.close()
            return retval
        except (psycopg2.errors.OperationalError, psycopg2.errors.UniqueViolation, Exception) as e:
            db.rollback()
            default_log.exception(e)
            return DBApiExceptionResponse(error=str(e))
        finally:
            if db is not None:
                db.close()
    return decorated_function