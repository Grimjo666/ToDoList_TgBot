from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from database import control_db
from ..keyboards import del_menu


class DeleteTask(StatesGroup):
    number = State()


async def delete_all_tasks(message: types.Message):
    control_db.delete_all(message.from_user.id)
    await message.answer('Задачи удалены')


async def waiting_del_number(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(text='Отправьте номер(а) задач(и) и нажмите удалить.\n'\
                                     'Формат: "0", "0-0", "0, 0, 0 ..."',
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=del_menu)
    await DeleteTask.number.set()


async def delete_task(message: types.Message, state: FSMContext):
    await message.answer('хэндлер делит сработал')


async def stop_state(message: types.Message, state: FSMContext):
    await message.answer('Отменено')
    await state.finish()


def register_handlers_delete_tasks(dp: Dispatcher):
    dp.register_callback_query_handler(stop_state, lambda c: c.data == 'button_cancel', state='*')
    dp.register_message_handler(delete_all_tasks, commands=['delete_all'])
    dp.register_callback_query_handler(waiting_del_number, lambda c: c.data == 'button_delete_task_menu')
    dp.register_message_handler(delete_task, state=DeleteTask.number)
