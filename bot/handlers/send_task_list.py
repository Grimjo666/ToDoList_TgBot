from bot import bot
from aiogram import types, Dispatcher
from database import control_db
from ..keyboards import show_tasks_menu


def get_task_list(user_id: int) ->str:
    try:
        tasks_data = control_db.get_task(user_id)
        text = ''

        for task_tuple in tasks_data:
            text += f'- {task_tuple.task}\n'  # Получаем название задачи
            text += f'..{task_tuple.task_description}\n' if task_tuple.task_description else ""  # Получаем описание задачи
            text += f'..{task_tuple.task_due_date}\n' if task_tuple.task_due_date else ""  # Получаем дедлайн задачи

        return text
    except:
        pass


# Отправляем список задач пользователю(изменяем текст меню)
async def send_task_list(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    try:
        text = get_task_list(callback_query.from_user.id)

        await bot.edit_message_text(text=text,
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=show_tasks_menu)

    except:
        await callback_query.answer('Список задач пуст')


async def command_send_task_list(message: types.Message):
    try:
        text = get_task_list(message.from_user.id)
        await message.answer(text)

    except:
        await message.answer('Список задач пуст')


def register_handlers_send_task(dp: Dispatcher):
    dp.register_callback_query_handler(send_task_list, lambda c: c.data == 'button_show_tasks')
    dp.register_message_handler(command_send_task_list, commands=['show_tasks'])