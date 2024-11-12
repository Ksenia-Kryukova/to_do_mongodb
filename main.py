from fastapi import FastAPI, HTTPException
from models import ToDo
from db import Db


app = FastAPI()
db = Db()


@app.post("/create_task")
async def create_task(task: ToDo):
    new_task = await db.create_task(task)
    return new_task


@app.get("/todo_list")
async def todo_list():
    tasks = await db.todo_list()
    return tasks


@app.get("/read_task/{task_id}")
async def read_task(task_id: str):
    task = await db.read_task(task_id)
    return task


@app.put("/update_task/{task_id}")
async def update_task(task_id: str, task: ToDo):
    update_task = await db.update_task(task_id, task)
    return update_task


@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    await db.delete_task(task_id)
    return {"Задача успешно удалена"}
