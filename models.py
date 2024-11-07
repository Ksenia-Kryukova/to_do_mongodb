from pydantic import BaseModel


class ToDo(BaseModel):
    _id: str | None = None
    title: str
    description: str
    completed: bool = False
