from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# кнопки
button_close = InlineKeyboardButton('❌', callback_data='button_close')

button_show_tasks = InlineKeyboardButton('Список задач', callback_data='button_show_tasks')
button_add_task = InlineKeyboardButton('Добавить задачу', callback_data='button_add_task')
button_delete_task_menu = InlineKeyboardButton('Удалить задачу', callback_data='button_delete_task_menu')
button_done = InlineKeyboardButton('Задача выполнена', callback_data='button_done')
button_main_menu = InlineKeyboardButton('В главное меню', callback_data='button_main_menu')

# Главное меню бота
task_menu = InlineKeyboardMarkup()

task_menu.add(button_show_tasks, button_add_task, button_delete_task_menu, button_close, button_done)


# Меню удаления сообщений
del_menu = InlineKeyboardMarkup(row_width=1)

del_btn = InlineKeyboardButton('Удалить', callback_data='button_delete_task')

del_menu.add(del_btn,button_main_menu, button_close)

