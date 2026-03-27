from app.database.models import async_session
from app.database.models import Task
from sqlalchemy import update


async def update_task_title(id: int, title: str):
    async with async_session() as session:
        await session.execute(
            update(Task).where(Task.id == id).values(title=title)
        )
        await session.commit()


async def update_task_description(id: int, description: str):
    async with async_session() as session:
        await session.execute(
            update(Task).where(Task.id == id).values(description=description)
        )
        await session.commit()


async def update_task_points_count(id: int, points_count: int):
    async with async_session() as session:
        await session.execute(
            update(Task).where(Task.id == id).values(points_count=points_count)
        )
        await session.commit()