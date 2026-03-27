from app.database.models import async_session
from app.database.models import OutfitUser


async def set_outfit_user(
        tg_id: int,
        outfit_id: int,
        grade: str
):
    async with async_session() as session:
        session.add(OutfitUser(
            tg_id=tg_id,
            outfit_id=outfit_id,
            grade=grade
        ))
        await session.commit()