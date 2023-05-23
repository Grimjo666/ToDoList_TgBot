from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re

from bot import bot
from database import control_db
from ..keyboards import del_menu


class DeleteTask(StatesGroup):
    number = State()


async def delete_all_tasks(callback_query: types.CallbackQuery):

    control_db.delete_all(callback_query.from_user.id)
    await callback_query.answer('Задачи удалены')


# Создаём и отправляем список задач и ждём номер задачи для удаления
async def waiting_del_number(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    user_id = callback_query.from_user.id
    text = 'Отправьте ID задач(и) и нажмите удалить.\n' \
           'Формат: "0",  "0 0 0..."\n\n'

    tasks_data = control_db.get_task(user_id=user_id)  # Получаем именованный кортеж с данными о задачах

    # Проходимся по кортежу для добавления в текс задач
    for task_tuple in tasks_data:
        text += f'{task_tuple.task} | ID - {task_tuple.id}\n'

    await bot.edit_message_text(text=text,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=del_menu)

    # Загружаем в FSM текс и ID текста для динамического изменения текста при удалении задачи
    await state.update_data(text_del_menu=text, message_id=message_id)
    await DeleteTask.number.set()


# Хэндлер для удаления задач по запросу пользователя
async def delete_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text_del_menu')
    message_id = data.get('message_id')

    chat_id = message.chat.id
    user_id = message.from_user.id
    task_id = message.text
    user_message_id = message.message_id

    # удаляем инфу из БД при формате ID записи '0'
    if re.fullmatch(r'\d+', task_id):
        try:
            control_db.delete(user_id, int(task_id))
            text = re.sub(fr'.+\| ID - {int(task_id)}', r'---', text)
        except:
            await message.answer('Не корректный ID задачи')
        # удаляем инфу из БД при формате ID записи '0 0 0...'
    elif re.search(r'\d \d', task_id):
        for num in re.split(r'[, ]+', task_id):
            try:
                control_db.delete(user_id, int(num))
                text = re.sub(fr'.+\| ID - {num}', r'---', text)

            except:
                await message.answer('Не корректный ID задачи')

    else:
        await message.answer('Не корректный ID задачи')

    await bot.edit_message_text(text=text,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=del_menu)

    await bot.delete_message(chat_id=chat_id, message_id=user_message_id)
    await state.update_data(text_del_menu=text)


def register_handlers_delete_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(delete_all_tasks, lambda c: c.data == 'button_delete_all')
    dp.register_callback_query_handler(waiting_del_number, lambda c: c.data == 'button_delete_task_menu')
    dp.register_message_handler(delete_task, state=DeleteTask.number)
