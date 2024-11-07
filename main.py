from fastapi import FastAPI
from models import ToDo
from uuid import uuid4
from db import collection


app = FastAPI()


@app.post("/create_task")
async def create_task(task: ToDo):
    new_task = task.__dict__.copy()
    new_task["_id"] = str(uuid4())
    collection.insert_one(new_task)
    return new_task


@app.get("/todo_list")
async def todo_list():
    tasks = []
    for task in collection.find():
        tasks.append(task)
    return tasks


@app.get("/read_task/{task_id}")
async def read_task(task_id: str):
    try:
        task = collection.find_one({"_id": task_id})
        return task
    except Exception:
        return {"Задача отсутствует в списке"}


@app.put("/update_task/{task_id}")
async def update_task(task_id: str, task: ToDo):
    try:
        collection.update_one({"_id": task_id}, {"$set": task.__dict__})
        return collection.find_one({"_id": task_id})
    except Exception:
        return {"Задача отсутствует в списке"}


@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    try:
        collection.delete_one({"_id": task_id})
        return {"Задача успешно удалена"}
    except Exception:
        return {"Задача отсутствует в списке"}
