from fastapi import HTTPException


class InvalidTaskDataException(HTTPException):
    def __init__(self, detail: str = "Такая задача уже существует") -> None:
        super().__init__(status_code=400, detail=detail)


class TaskNotFound(HTTPException):
    def __init__(self, detail: str = "Такой задачи не существует") -> None:
        super().__init__(status_code=404, detail=detail)
