from app.database.models import async_session
from app.database.models import PromoCode


async def set_promo_code(promo_code: str):
    async with async_session() as session:
        session.add(PromoCode(promo_code=promo_code))
        await session.commit()