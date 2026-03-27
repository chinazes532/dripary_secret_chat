from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from config import config


class MemberProtect(BaseMiddleware):
    async def __call__(
            self,
            handler,
            event: TelegramObject,
            data: dict
    ):
        user = getattr(event, "from_user", None)
        if not user:
            return await handler(event, data)

        member = await event.bot.get_chat_member(
            chat_id=config.bot.chat_id,
            user_id=event.from_user.id
        )

        if member.status in ["member", "creator", "administrator"]:
            return await handler(event, data)

        if hasattr(event, "answer"):
            await event.answer("У вас недостаточно прав!")
            return None
        return None
