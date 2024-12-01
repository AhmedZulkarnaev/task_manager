import datetime
from enum import Enum


class Priority(Enum):
    LOW = "низкий"
    MEDIUM = "средний"
    HIGH = "высокий"


class Task:
    def __init__(self, title, description, category, priority: Priority, status=1, due_date=None):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.due_date = due_date if due_date else "Нет информации"

    def __repr__(self) -> str:
        status_str = 'Выполнена' if self.status == 2 else 'Не выполнена'
        return (f"Информация о задаче:\n"
                f"Название: {self.title}\n"
                f"Описание: {self.description}\n"
                f"Категория: {self.category}\n"
                f"Срок выполнения: {self.due_date}\n"
                f"Приоритет: {self.priority.value}\n"
                f"Статус: {status_str}\n")
