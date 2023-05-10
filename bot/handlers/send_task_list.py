from bot import bot
from aiogram import types, Dispatcher
from database import control_db


# Собираем сообщение из списка get_task и отправляем пользователю
async def send_task_list(message: types.Message):
    try:
        tasks = control_db.get_task(message.from_user.id)
        message_from_user = ''
        # tasks = (filter(lambda x: x is not None, task) for task in tasks)
        for task in tasks:
            for elem in task:
                if elem is not None:
                    message_from_user += elem + '\n'
            message_from_user += '\n'

        await bot.send_message(message.chat.id, message_from_user)

    except:
        await bot.send_message(message.chat.id, 'Список задач пуст')


def register_handlers_send_task(dp: Dispatcher):
    dp.register_message_handler(send_task_list, commands=['show_tasks'])