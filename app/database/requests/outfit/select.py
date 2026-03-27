from app.database.models import async_session
from app.database.models import Outfit
from sqlalchemy import select


async def get_outfit_by_id(id: int):
    async with async_session() as session:
        outfit = await session.scalar(select(Outfit).where(Outfit.id == id))
        return outfit

