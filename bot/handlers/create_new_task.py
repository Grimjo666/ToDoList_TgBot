from bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import control_db


class NewTask(StatesGroup):
    name = State()


# Запрашиваем названия для нового списка от пользователя
async def request_task_name(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, text='Добавь задачу (введи текст)')

    await NewTask.name.set()


# Переходим в состояние записи задачи
async def create_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    task_name = message.text
    control_db.write_task(user_id, task_name)

    await message.answer('Задача успешно добавлена')
    await state.finish()


def register_handlers_create_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(request_task_name, lambda c: c.data == 'button_add_task')
    dp.register_message_handler(create_task, state=NewTask.name)
