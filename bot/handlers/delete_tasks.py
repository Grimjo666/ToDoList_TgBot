from aiogram import types, Dispatcher
from database import control_db


async def delete_all_tasks(message: types.Message):
    control_db.delete_all(message.from_user.id)


def register_handlers_delete_tasks(dp: Dispatcher):
    dp.register_message_handler(delete_all_tasks, commands=['delete_all'])