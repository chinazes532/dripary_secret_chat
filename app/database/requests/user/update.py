from app.database.models import async_session
from app.database.models import User
from sqlalchemy import update


async def update_user_balance(tg_id: int, balance: int):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(balance=User.balance + balance)
        )
        await session.commit()


async def update_user_game_points(tg_id: int, game_points: int):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(game_points=User.game_points + game_points)
        )
        await session.commit()