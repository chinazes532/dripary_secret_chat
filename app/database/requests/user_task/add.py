from app.database.models import async_session
from app.database.models import UserTask


async def set_user_task(tg_id: int, task_id: int, date: str):
    async with async_session() as session:
        session.add(UserTask(tg_id=tg_id,
                             task_id=task_id,
                             date=date))
        await session.commit()