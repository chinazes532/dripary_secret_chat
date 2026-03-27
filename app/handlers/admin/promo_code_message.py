from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.promo_code.add import set_promo_code
from app.database.requests.promo_code.select import get_promo_code_by_id
from app.database.requests.promo_code.delete import delete_promo_code_by_id

from app.states import AddPromoCode

promo_code = Router()


@promo_code.callback_query(F.data == "promo_codes")
async def promo_codes(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Добавленные промокоды:</b>",
        reply_markup=await bkb.promo_codes_cb()
    )


@promo_code.callback_query(F.data == "add_code")
async def add_code(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Пришлите промокод:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddPromoCode.promo_code)


@promo_code.message(AddPromoCode.promo_code)
async def check_promo_code(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 300:
        await set_promo_code(message.text)

        await message.answer(
            "<b>Промокод был успешно добавлен!</b>",
            reply_markup=await bkb.promo_codes_cb()
        )

        await state.clear()

    else:
        await message.answer("<b>Промокод должен быть до 300 символов!</b>",
                             reply_markup=ikb.admin_cancel)


@promo_code.callback_query(F.data.startswith("code_"))
async def check_promo_code_info(callback: CallbackQuery):
    code_id = int(callback.data.split("_")[1])
    code = await get_promo_code_by_id(code_id)

    await callback.message.edit_text(
        f"<b>Панель управления промокодом</b>\n\n"
        f"<b>Промокод:</b> <code>{code.promo_code}</code>\n\n"
        f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_promo_code(code_id)
    )


@promo_code.callback_query(F.data.startswith("deletecode_"))
async def delete_promo_code(callback: CallbackQuery):
    code_id = int(callback.data.split("_")[1])
    await delete_promo_code_by_id(code_id)

    await callback.message.edit_text(
        "<b>Промокод был успешно удален!</b>",
        reply_markup=await bkb.promo_codes_cb()
    )

