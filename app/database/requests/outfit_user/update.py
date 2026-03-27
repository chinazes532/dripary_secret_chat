from app.database.models import async_session
from app.database.models import OutfitUser
from sqlalchemy import update


async def update_user_outfit_grade(tg_id: int, outfit_id: int, grade: str):
    async with async_session() as session:
        await session.execute(
            update(OutfitUser).where(
                OutfitUser.tg_id == tg_id,
                OutfitUser.outfit_id == outfit_id
            ).values(grade=grade)
        )
        await session.commit()