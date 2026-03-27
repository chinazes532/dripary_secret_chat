import logging
import random
from datetime import datetime, timedelta

from app.database.models import async_session, User, Task
from app.database.models import UserTask
from sqlalchemy import select, func

logger = logging.getLogger(__name__)


async def get_user_task(tg_id: int, task_id: int):
    async with async_session() as session:
        task = await session.scalar(select(UserTask).where(
            UserTask.tg_id == tg_id,
            UserTask.task_id == task_id
        ))
        return task


async def get_user_tasks(tg_id: int):
    async with async_session() as session:
        tasks = await session.execute(select(UserTask).where(UserTask.tg_id == tg_id))
        return tasks


async def get_random_top_user_this_week(top_limit: int = 5):
    async with async_session() as session:
        now = datetime.now()

        # начало недели (понедельник)
        start_of_week = now - timedelta(days=now.weekday())

        # конец недели
        end_of_week = start_of_week + timedelta(days=7)

        result = await session.execute(
            select(
                User.first_name,
                User.tg_id,
                func.sum(Task.points_count).label("points")
            )
            .join(UserTask, UserTask.tg_id == User.tg_id)
            .join(Task, Task.id == UserTask.task_id)
            .where(
                func.to_date(UserTask.date, 'DD.MM.YYYY') >= start_of_week
            )
            .where(
                func.to_date(UserTask.date, 'DD.MM.YYYY') < end_of_week
            )
            .group_by(User.tg_id, User.first_name)
            .order_by(func.sum(Task.points_count).desc())
            .limit(top_limit)
        )

        top_users = result.all()

        if not top_users:
            return None

        # случайный победитель из топа
        return random.choice(top_users)

async def get_top_users(period: str = "all", limit: int = 10):
    async with async_session() as session:
        now = datetime.now()

        query = (
            select(
                User.first_name,
                User.tg_id,
                func.sum(Task.points_count).label("points")
            )
            .join(UserTask, UserTask.tg_id == User.tg_id)
            .join(Task, Task.id == UserTask.task_id)
        )

        # 📅 фильтрация
        if period == "day":
            start = now.strftime("%Y-%m-%d")
            query = query.where(UserTask.date >= start)

        elif period == "week":
            start_of_week = now - timedelta(days=now.weekday())
            start = start_of_week.strftime("%Y-%m-%d")
            query = query.where(UserTask.date >= start)

        elif period == "all":
            pass

        result = await session.execute(
            query
            .group_by(User.tg_id, User.first_name)
            .order_by(func.sum(Task.points_count).desc())
            .limit(limit)
        )

        return result.all()
