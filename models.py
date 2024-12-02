from enum import Enum


class Priority(Enum):
    LOW = "низкий"
    MEDIUM = "средний"
    HIGH = "высокий"


class Task:
    def __init__(self, title, description, category, priority: Priority, status="Не выполнена", due_date=None):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.due_date = due_date if due_date else "Нет информации"

    def __repr__(self) -> str:
        return (f"Информация о задаче:\n"
                f"Название: {self.title}\n"
                f"Описание: {self.description}\n"
                f"Категория: {self.category}\n"
                f"Срок выполнения: {self.due_date}\n"
                f"Приоритет: {self.priority.value}\n"
                f"Статус: {self.status}\n")