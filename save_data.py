import json
from typing import List

from models import Task, Priority
from database import get_tasks

tasks = get_tasks()


class TaskEncoder(json.JSONEncoder):
    """Кастомный JSON-энкодер для сериализации объектов Task."""
    def default(self, obj):
        if isinstance(obj, Task):
            return {
                "id": obj.id,
                "title": obj.title,
                "description": obj.description,
                "category": obj.category,
                "due_date": obj.due_date,
                "priority": obj.priority,
                "status": obj.status,
            }
        return super().default(obj)


def save_tasks_to_json(tasks: List[Task], filename: str) -> None:
    """Сохраняет задачи в файл JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4, cls=TaskEncoder)


def load_tasks_from_json(filename: str) -> List[Task]:
    """Загружает задачи из файла JSON."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [
        Task(
            id=item["id"],
            title=item["title"],
            description=item["description"],
            category=item["category"],
            priority=Priority(item["priority"]),
            status=item["status"],
            due_date=item.get("due_date"),
        )
        for item in data
    ]


save_tasks_to_json(tasks, "tasks.json")

loaded_tasks = load_tasks_from_json("tasks.json")
