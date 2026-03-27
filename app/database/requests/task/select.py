from app.database.models import async_session
from app.database.models import Task
from sqlalchemy import select


async def get_tasks():
    async with async_session() as session:
        tasks = await session.scalars(select(Task))
        return tasks


async def get_task_by_id(id: int):
    async with async_session() as session:
        task = await session.scalar(select(Task).where(Task.id == id))
        return task