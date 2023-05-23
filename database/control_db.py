import sqlite3
from collections import namedtuple


# Функция для записи задач в БД
def write_task(user_id: int, name, description=None, task_due_date=None):
    base = sqlite3.connect('database/todo_data.db')
    cur = base.cursor()

    base.execute('''CREATE TABLE IF NOT EXISTS todo_tasks(
                    id INTEGER PRIMARY KEY, 
                    user_id INTEGER ,
                    task,
                    task_description,
                    task_due_date)''')
    base.commit()

    cur.execute('''INSERT INTO todo_tasks (
                    user_id,
                    task,
                    task_description,
                    task_due_date) VALUES (?, ?, ?, ?)''', (user_id, name, description, task_due_date))
    base.commit()
    cur.close()
    base.close()


# Функция для получения списка задач из БД
def get_task(user_id: int) -> list[namedtuple]:

    Tasks_data = namedtuple('Tasks_data', ['id', 'task', 'task_description', 'task_due_date'])

    base = sqlite3.connect('database/todo_data.db')
    cur = base.cursor()
    cur.execute("SELECT id, task, task_description, task_due_date FROM todo_tasks WHERE user_id == ?", (user_id,))

    tasks_list = list()
    for item in  cur.fetchall():
        tasks_list.append(Tasks_data(*item))

    cur.close()
    base.close()
    return tasks_list


# Удаление задачи из БД
def delete(user_id: int, id):
    base = sqlite3.connect('database/todo_data.db')
    cur = base.cursor()

    cur.execute("DELETE FROM todo_tasks WHERE user_id == ? AND id == ?", (user_id, id))

    base.commit()
    cur.close()
    base.close()


# Удаление всех задач из БД
def delete_all(user_id: int):
    base = sqlite3.connect('database/todo_data.db')
    cur = base.cursor()

    cur.execute("DELETE FROM todo_tasks WHERE user_id == ?", (user_id,))
    base.commit()
    cur.close()
    base.close()
