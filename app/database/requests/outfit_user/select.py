from app.database.models import async_session
from app.database.models import OutfitUser
from sqlalchemy import select


async def get_outfit_user(tg_id: int, outfit_id: int):
    async with async_session() as session:
        user = await session.scalar(
            select(OutfitUser).where(
                OutfitUser.tg_id == tg_id,
                OutfitUser.outfit_id == outfit_id,
            )
        )
        return user