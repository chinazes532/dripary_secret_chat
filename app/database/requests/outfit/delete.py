from app.database.models import async_session
from app.database.models import Outfit, OutfitUser
from sqlalchemy import delete


async def delete_outfit_by_id(outfit_id: int):
    async with async_session() as session:
        await session.execute(
            delete(OutfitUser).where(OutfitUser.outfit_id == outfit_id)
        )

        await session.execute(
            delete(Outfit).where(Outfit.id == outfit_id)
        )

        await session.commit()