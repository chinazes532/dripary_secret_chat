from app.database.models import async_session
from app.database.models import Outfit


async def set_outfit(tg_id: int, file_id: str,
                     message_id: int ,likes: int = 0,
                     dislikes: int = 0) -> int:
    async with async_session() as session:
        outfit = Outfit(tg_id=tg_id,
                        file_id=file_id,
                        message_id=message_id,
                        likes=likes,
                        dislikes=dislikes)
        session.add(outfit)
        await session.flush()
        outfit_id = outfit.id
        await session.commit()
        return outfit_id