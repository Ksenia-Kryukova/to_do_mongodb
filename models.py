from pydantic import BaseModel


class ToDo(BaseModel):
    title: str
    description: str
    completed: bool = False


class Task(BaseModel):
    _id: str
    title: str
    description: str
    completed: bool = False


class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str
