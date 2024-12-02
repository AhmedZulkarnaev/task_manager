import sqlite3
from typing import List

from models import Task

conn = sqlite3.connect('Tasks.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def create_table():
    """Создает таблицу task, если она не существует."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            due_date INTEGER,
            priority TEXT,
            status TEXT NOT NULL
        )
    """)


create_table()


def insert_task(task: Task):
    """Вставляет задачу в таблицу task."""
    with conn:
        cur.execute(""" 
            INSERT INTO tasks (title, description, category, due_date, priority, status) 
            VALUES (:title, :description, :category, :due_date, :priority, :status)
        """, {
            'title': task.title,
            'description': task.description,
            'category': task.category,
            'due_date': task.due_date,
            'priority': task.priority.value,
            'status': task.status
        })


def get_tasks(category: str = None, status: str = None) -> List[Task]:
    """Получает задачи по категории или статусу, если указано."""
    query = "SELECT * FROM tasks"
    parameters = {}

    if category and status:
        query += " WHERE category = :category AND status = :status"
        parameters = {'category': category, 'status': status}
    elif category:
        query += " WHERE category = :category"
        parameters = {'category': category}
    elif status:
        query += " WHERE status = :status"
        parameters = {'status': status}

    cur.execute(query, parameters)
    results = cur.fetchall()
    tasks = []
    for result in results:
        task = Task(
            title=result["title"],
            description=result["description"],
            category=result["category"],
            due_date=result["due_date"],
            priority=result["priority"],
            status=result["status"]
        )
        tasks.append(task)
    return tasks



def get_tasks_by_category(category: str) -> List[Task]:
    """Поиск по категории."""
    cur.execute("SELECT * FROM tasks WHERE category = ?", (category,))
    results = cur.fetchall()
    return [Task(*result) for result in results]


def get_tasks_by_status(status: str) -> List[Task]:
    """Поиск по статусу."""
    cur.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    results = cur.fetchall()
    return [Task(*result) for result in results]


def search_tasks(keyword: str) -> List[Task]:
    """Поиск по ключевым словам."""
    cur.execute(
        "SELECT * FROM tasks WHERE title LIKE ?", f"%{keyword}%"
    )
    results = cur.fetchall()
    return [Task(*result) for result in results]


def delete_task(task_id: int = None, category: str = None):
    """
    Удаляет задачи на основе переданных критериев.

    :param task_id: ID задачи (если указан).
    :param category: Категория задачи (если указана).
    """
    if task_id is None and category is None:
        raise ValueError("Необходимо указать task_id или category.")

    if task_id:
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if category:
        cur.execute("DELETE FROM tasks WHERE category = ?", (category,))
    conn.commit()


def update_task(task_id: int, **fields):
    """Позволяет редактировать задачу."""
    fields = {k: v for k, v in fields.items() if v is not None}
    set_clause = ", ".join(f"{key} = :{key}" for key in fields.keys())
    fields["id"] = task_id

    with conn:
        cur.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = :id",
            fields
        )
