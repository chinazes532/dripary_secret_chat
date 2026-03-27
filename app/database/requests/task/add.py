from app.database.models import async_session
from app.database.models import Task


async def set_task(
        title: str,
        description: str,
        points_count: int
):
    async with async_session() as session:
        session.add(Task(title=title,
                         description=description,
                         points_count=points_count))
        await session.commit()