from bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import control_db


class NewTask(StatesGroup):
    name = State()
    descriptions = State()


# Запрашиваем названия для нового списка от пользователя
async def request_task_name(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Добавь задачу (введи текст)')
    await NewTask.name.set()


# Запрашиваем описание для нового списка от пользователя
async def request_task_description(massage: types.Message, state: FSMContext):
    await bot.send_message(chat_id=massage.chat.id, text='Добавь описание задачи(не обязательно)')
    await state.update_data(task_name=massage.text)
    await NewTask.descriptions.set()


# Переходим в состояние записи задачи
async def create_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    task_name = data.get('task_name')
    task_description = message.text
    control_db.write_task(user_id, task_name, task_description)

    await message.answer('Задача успешно добавлена')
    await state.finish()


def register_handlers_create_tasks(dp: Dispatcher):
    dp.register_message_handler(request_task_name, commands=['create_new_task'])
    dp.register_message_handler(request_task_description, state=NewTask.name)
    dp.register_message_handler(create_task, state=NewTask.descriptions)
