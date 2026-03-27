from app.database.models import async_session
from app.database.models import Giveaway
from sqlalchemy import select


async def get_giveaway(id: int):
    async with async_session() as session:
        giveaway = await session.scalar(
            select(Giveaway)
            .where(Giveaway.id == id)
        )
        return giveaway