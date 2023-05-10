from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

task_menu = InlineKeyboardMarkup()

btn1 = InlineKeyboardButton('Список задач', callback_data='button_show_tasks')
btn2 = InlineKeyboardButton('Добавить задачу', callback_data='button_add_task')
btn3 = InlineKeyboardButton('Удалить задачу', callback_data='button_delete_task')
btn4 = InlineKeyboardButton('Удалить все задачи', callback_data='button_delete_all_task')
btn5 = InlineKeyboardButton('❌', callback_data='button_close')

task_menu.add(btn1, btn2, btn3, btn4, btn5)