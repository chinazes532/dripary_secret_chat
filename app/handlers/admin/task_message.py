from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.task.add import set_task
from app.database.requests.task.select import get_task_by_id
from app.database.requests.task.update import (update_task_title, update_task_description,
                                               update_task_points_count)
from app.database.requests.task.delete import delete_task_by_id

from app.states import AddTask, EditTask


task = Router()


@task.callback_query(F.data == "all_tasks")
async def all_tasks(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Текущие задания:</b>",
        reply_markup=await bkb.tasks_cb()
    )


@task.callback_query(F.data == "add_task")
async def add_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>Введите заголовок для задания:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(AddTask.title)


@task.message(AddTask.title)
async def check_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 100:
        await state.update_data(title=message.text)

        await message.answer(
            "<b>Введите описание для задания:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddTask.description)

    else:
        await message.answer("Заголовок должен быть до 100 символов!",
                             reply_markup=ikb.admin_cancel)


@task.message(AddTask.description)
async def check_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await state.update_data(description=message.html_text)

        await message.answer(
            "<b>Введите стоимость выполнения задания:</b>",
            reply_markup=ikb.admin_cancel
        )

        await state.set_state(AddTask.points_count)

    else:
        await message.answer("Описание должно быть до 1000 символов!",
                             reply_markup=ikb.admin_cancel)


@task.message(AddTask.points_count)
async def check_points_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(points_count=int(message.text))

        data = await state.get_data()

        title = data.get('title')
        description = data.get('description')
        points_count = data.get('points_count')

        await set_task(title, description, points_count)

        await message.answer("<b>Задание было успешно добавлено!</b>",
                             reply_markup=await bkb.tasks_cb())

        await state.clear()

    else:
        await message.answer("Стоимость задания должна быть числом больше нуля!",
                             reply_markup=ikb.admin_cancel)


@task.callback_query(F.data.startswith("task_"))
async def check_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    task_info = await get_task_by_id(task_id)

    await callback.message.edit_text(
        f"<b>Панель управления заданием</b>\n\n"
        f"<b>Заголовок:</b> {task_info.title}\n"
        f"<b>Описание:</b> {task_info.description}\n"
        f"<b>Стоимость:</b> {task_info.points_count} Street Credits\n\n"
        f"<i>Выберите действие:</i>",
        reply_markup=await bkb.edit_task(task_info.id)
    )


@task.callback_query(F.data.startswith("edit_task_title_"))
async def edit_task_title(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("_")[3])

    await callback.message.edit_text(
        "<b>Введите новый заголовок для задания:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditTask.new_title)
    await state.update_data(id=task_id)


@task.message(EditTask.new_title)
async def check_new_title(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 100:
        await state.update_data(title=message.text)

        data = await state.get_data()

        id = data.get('id')
        title = data.get('title')

        await update_task_title(id, title)
        task_info = await get_task_by_id(id)

        await message.answer(
            f"<b>Панель управления заданием</b>\n\n"
            f"<b>Заголовок:</b> {task_info.title}\n"
            f"<b>Описание:</b> {task_info.description}\n"
            f"<b>Стоимость:</b> {task_info.points_count} Street Credits\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_task(task_info.id)
        )

        await state.clear()

    else:
        await message.answer("Заголовок должен быть до 100 символов!",
                             reply_markup=ikb.admin_cancel)


@task.callback_query(F.data.startswith("edit_task_description_"))
async def edit_task_description(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("_")[3])

    await callback.message.edit_text(
        "<b>Введите новое описание для задания:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditTask.new_description)
    await state.update_data(id=task_id)


@task.message(EditTask.new_description)
async def check_new_description(message: Message, state: FSMContext):
    if message.text and len(message.text) <= 1000:
        await state.update_data(description=message.html_text)

        data = await state.get_data()

        id = data.get('id')
        description = data.get('description')

        await update_task_description(id, description)
        task_info = await get_task_by_id(id)

        await message.answer(
            f"<b>Панель управления заданием</b>\n\n"
            f"<b>Заголовок:</b> {task_info.title}\n"
            f"<b>Описание:</b> {task_info.description}\n"
            f"<b>Стоимость:</b> {task_info.points_count} Street Credits\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_task(task_info.id)
        )

        await state.clear()

    else:
        await message.answer("Описание должно быть до 1000 символов!",
                             reply_markup=ikb.admin_cancel)


@task.callback_query(F.data.startswith("edit_task_price_"))
async def edit_task_price(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("_")[3])

    await callback.message.edit_text(
        "<b>Введите новую стоимость для задания:</b>",
        reply_markup=ikb.admin_cancel
    )

    await state.set_state(EditTask.new_points_count)
    await state.update_data(id=task_id)


@task.message(EditTask.new_points_count)
async def check_new_points_count(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        await state.update_data(points_count=int(message.text))

        data = await state.get_data()

        id = data.get('id')
        points_count = data.get('points_count')

        await update_task_points_count(id, points_count)
        task_info = await get_task_by_id(id)

        await message.answer(
            f"<b>Панель управления заданием</b>\n\n"
            f"<b>Заголовок:</b> {task_info.title}\n"
            f"<b>Описание:</b> {task_info.description}\n"
            f"<b>Стоимость:</b> {task_info.points_count} Street Credits\n\n"
            f"<i>Выберите действие:</i>",
            reply_markup=await bkb.edit_task(task_info.id)
        )

        await state.clear()

    else:
        await message.answer("Стоимость задания должна быть числом больше нуля!",
                             reply_markup=ikb.admin_cancel)


@task.callback_query(F.data.startswith("delete_task_"))
async def delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[2])
    await delete_task_by_id(task_id)

    await callback.message.edit_text(
        "<b>Задание было успешно удалено!</b>",
        reply_markup=await bkb.tasks_cb()
    )
