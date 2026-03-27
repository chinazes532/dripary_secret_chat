from app.database.models import async_session
from app.database.models import Outfit
from sqlalchemy import update


async def increment_outfit_likes(id: int):
    async with async_session() as session:
        await session.execute(
            update(Outfit).where(Outfit.id == id).values(likes=Outfit.likes+1)
        )
        await session.commit()


async def increment_outfit_dislikes(id: int):
    async with async_session() as session:
        await session.execute(
            update(Outfit).where(Outfit.id == id).values(dislikes=Outfit.dislikes+1)
        )
        await session.commit()


async def update_outfit_message_id(id: int, message_id: int):
    async with async_session() as session:
        await session.execute(
            update(Outfit).where(Outfit.id == id).values(message_id=message_id)
        )
        await session.commit()


async def decrement_outfit_likes(id: int):
    async with async_session() as session:
        await session.execute(
            update(Outfit)
            .where(Outfit.id == id)
            .values(likes=Outfit.likes - 1)
        )
        await session.commit()


async def decrement_outfit_dislikes(id: int):
    async with async_session() as session:
        await session.execute(
            update(Outfit)
            .where(Outfit.id == id)
            .values(dislikes=Outfit.dislikes - 1)
        )
        await session.commit()