import logging
from aiogram import executor, types

from bot import dp, bot, task_menu

# Хэндлеры
from bot import create_new_task, send_task_list, delete_tasks

logging.basicConfig(level=logging.INFO)


# Обработчик команды старт
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    start_text = 'Я ToDo-bot, созданный что бы помочь тебе повысить твою продуктивность\n\n'\
                 'Вот список моих команд:\n'\
                 '/start, /help - вызывает это сообщение\n'\
                 '/delete_all - удалить все задачи'

    await bot.send_message(chat_id=message.chat.id,
                           text=start_text,
                           reply_markup=task_menu)


create_new_task.register_handlers_create_tasks(dp)
send_task_list.register_handlers_send_task(dp)
delete_tasks.register_handlers_delete_tasks(dp)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
