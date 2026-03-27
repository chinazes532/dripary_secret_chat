from app.database.models import async_session
from app.database.models import Task
from sqlalchemy import delete


async def delete_task_by_id(id: int):
    async with async_session() as session:
        await session.execute(
            delete(Task).where(Task.id == id)
        )
        await session.commit()