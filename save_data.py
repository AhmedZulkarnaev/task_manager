import json
from typing import List

from models import Task


def save_tasks_to_json(tasks: List[Task], file_path: str):
    """Сохраняет задачи в файл JSON."""
    with open(file_path, "w", encoding="utf-8") as file:
        tasks_list = []
        for i, task in enumerate(tasks, start=1):
            task_dict = {
                "id": i,
                "title": task.title,
                "description": task.description,
                "category": task.category,
                "due_date": task.due_date,
                "priority": task.priority,
                "status": task.status
            }
            tasks_list.append(task_dict)
        json.dump(tasks_list, file, ensure_ascii=False, indent=4)

