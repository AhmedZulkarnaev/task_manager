import sqlite3
from typing import List
import datetime
from models import Task
from models import Priority

conn = sqlite3.connect('Tasks.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()


def create_table():
    """Создает таблицу task, если она не существует."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            category TEXT,
            due_date INTEGER,
            priority TEXT,
            status TEXT
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
            'priority': task.priority,
            'status': task.status
        })


def get_tasks() -> List[Task]:
    """Получает все задачи из таблицы task."""
    cur.execute("SELECT * FROM tasks")
    results = cur.fetchall()
    tasks = []
    for result in results:
        title = result["title"]
        description = result["description"]
        category = result["category"]
        priority = result["priority"]
        status = result["status"]
        task = Task(title=title, description=description, category=category, priority=priority, status=status)
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
    """Удаляет задачу из таблицы task по id или категории."""
    query = "DELETE FROM task WHERE"
    params = []

    if task_id:
        query += " id = ?"
        params.append(task_id)

    if category:
        if params:
            query += " OR"
        query += " category = ?"
        params.append(category)

    with conn:
        cur.execute(query, tuple(params))


def update_task(id: int, **fields):
    """Позволяет редактировать задачу."""
    fields = {k: v for k, v in fields.items() if v is not None}
    set_clause = ", ".join(f"{key} = :{key}" for key in fields.keys())
    fields["id"] = id

    with conn:
        cur.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = :id",
            fields
        )


def complete_task(id: int):
    """Помечает задачу как выполненную."""
    with conn:
        cur.execute(
            'UPDATE tasks SET status = "Выполнено", due_date = :due_date WHERE id = :id',
            {'id': id, 'due_date': datetime.datetime.now().isoformat()}
        )
