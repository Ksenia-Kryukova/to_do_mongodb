from fastapi import FastAPI, Request
from exceptions import InvalidTaskDataException, TaskNotFound
from fastapi.responses import JSONResponse
from models import ToDo, Task, ErrorResponseModel
from db import Db


app = FastAPI()
db = Db()


@app.exception_handler(InvalidTaskDataException)
async def invalid_task_data_exception(request: Request, ex: InvalidTaskDataException):
    error_response = ErrorResponseModel(
        status_code=ex.status_code,
        message=ex.detail,
        error_code="invalid_task_data"
    )
    return JSONResponse(
        status_code=ex.status_code,
        content=error_response.model_dump()
        )


@app.exception_handler(TaskNotFound)
async def task_not_found(request: Request, ex: TaskNotFound):
    error_response = ErrorResponseModel(
        status_code=ex.status_code,
        message=ex.detail,
        error_code="task_not_found"
    )
    return JSONResponse(
        status_code=ex.status_code,
        content=error_response.model_dump()
        )


@app.post("/create_task", response_model=Task)
async def create_task(task: ToDo):
    existing_task = await db.find_task_by_title(task.title)
    if existing_task:
        raise InvalidTaskDataException()
    new_task = await db.create_task(task)
    return new_task


@app.get("/todo_list")
async def todo_list():
    tasks = await db.todo_list()
    return tasks


@app.get("/read_task/{task_id}", response_model=Task)
async def read_task(task_id: str):
    task = await db.read_task(task_id)
    if task:
        return task
    else:
        raise TaskNotFound()


@app.put("/update_task/{task_id}", response_model=Task)
async def update_task(task_id: str, task: ToDo):
    update_task = await db.update_task(task_id, task)
    if update_task:
        return update_task
    else:
        raise TaskNotFound()


@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    task = await db.read_task(task_id)
    if task:
        await db.delete_task(task_id)
        return {"Задача успешно удалена"}
    else:
        raise TaskNotFound()
