from bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import control_db
from ..keyboards import add_menu


class NewTask(StatesGroup):
    name = State()


# Запрашиваем названия для нового списка от пользователя
async def request_task_name(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Добавь задачу (введи текст)',
                                reply_markup=add_menu)

    message_text = 'Добавь задачу (введи текст)\n\n' \
                   'Добавленные задачи:\n\n'

    await state.update_data(message_id=message_id, message_text=message_text)
    await NewTask.name.set()


# Переходим в состояние записи задачи
async def create_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    message_text = data.get('message_text')  # Переменная для реализации динамического текста меню

    chat_id = message.chat.id
    user_id = message.from_user.id
    task_name = message.text

    message_text += '-' + task_name + '\n'
    control_db.write_task(user_id, task_name)

    await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                text=message_text,
                                reply_markup=add_menu)

    await state.update_data(message_text=message_text)  # Записываем текс в FSM
    # Удаляем сообщение пользователя для чистоты чата
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)


def register_handlers_create_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(request_task_name, lambda c: c.data == 'button_add_task')
    dp.register_message_handler(create_task, state=NewTask.name)
