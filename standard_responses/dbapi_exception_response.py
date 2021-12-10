from pydantic.main import BaseModel, Optional


class DBApiExceptionResponse(BaseModel):
    error: str
    user_email: Optional[str]

