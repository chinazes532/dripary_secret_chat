from app.database.models import async_session
from app.database.models import PromoCode
from sqlalchemy import delete


async def delete_promo_code_by_id(id: int):
    async with async_session() as session:
        await session.execute(
            delete(PromoCode).where(PromoCode.id == id)
        )
        await session.commit()