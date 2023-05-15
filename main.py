import logging
from aiogram import executor, types
from aiogram.dispatcher import FSMContext

from bot import dp, bot, task_menu

# Хэндлеры
from bot import create_new_task, send_task_list, delete_tasks

logging.basicConfig(level=logging.INFO)


# # Хэндлер, присылающий основное меню через команду старт
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message, state: FSMContext):
    start_text = 'Я ToDo-bot, созданный что бы помочь тебе повысить твою продуктивность\n\n'\
                 'Вот список моих команд:\n'\
                 '/start, /help - вызывает это сообщение\n'\
                 '/delete_all - удалить все задачи'
    await state.update_data(start_text=start_text)

    await bot.send_message(chat_id=message.chat.id,
                           text=start_text,
                           reply_markup=task_menu)


# Хэндлер, присылающий основное меню по нажатию на кнопку
@dp.callback_query_handler(lambda c: c.data == 'button_main_menu')
async def send_main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    data = await state.get_data()
    start_text = data.get('start_text')

    await bot.edit_message_text(text=start_text,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=task_menu)


# Основной функционал бота
create_new_task.register_handlers_create_tasks(dp)
send_task_list.register_handlers_send_task(dp)
delete_tasks.register_handlers_delete_tasks(dp)


# Хэндлер для удаления сообщений бота
@dp.callback_query_handler(lambda c: c.data == 'button_close')
async def close_menu(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await state.finish()


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
