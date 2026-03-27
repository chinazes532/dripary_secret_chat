from app.database.models import async_session
from app.database.models import PromoCode
from sqlalchemy import select, func


async def get_promo_codes():
    async with async_session() as session:
        codes = await session.scalars(select(PromoCode))
        return codes


async def get_promo_code_by_id(id: int):
    async with async_session() as session:
        code = await session.scalar(select(PromoCode).where(PromoCode.id == id))
        return code


async def get_random_promo_code():
    async with async_session() as session:
        code = await session.execute(
            select(PromoCode).order_by(func.random()).limit(1)
        )
        return code.scalar_one_or_none()