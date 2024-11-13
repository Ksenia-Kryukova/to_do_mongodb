from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
from models import ToDo


class Db:
    def __init__(self):
        self.client = AsyncIOMotorClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]
        self.collection = self.db["mytodolist"]

    async def create_task(self, task: ToDo):
        new_task = task.model_dump()
        new_task["_id"] = str(uuid4())
        await self.collection.insert_one(new_task)
        return new_task

    async def todo_list(self):
        tasks = await list(self.collection.find())
        return tasks

    async def read_task(self, task_id: str):
        task = await self.collection.find_one({"_id": task_id})
        return task

    async def find_task_by_title(self, title: str):
        task = await self.collection.find_one({"title": title})
        return task

    async def update_task(self, task_id: str, task: ToDo):
        update_task = await self.collection.update_one(
            {"_id": task_id},
            {"$set": task.__dict__}
            )
        return update_task

    async def delete_task(self, task_id: str):
        await self.collection.delete_one({"_id": task_id})
