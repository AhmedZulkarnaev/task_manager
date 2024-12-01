import datetime
from enum import Enum


class Priority(Enum):
    LOW = "низкий"
    MEDIUM = "средний"
    HIGH = "высокий"


class Task:
    def __init__(self, title, category, description, priority: Priority, status=1, due_date=None):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.due_date = due_date if due_date else datetime.datetime.utcnow()

    def __repr__(self) -> str:
        return (f"Task(title={self.title}, description={self.description}, category={self.category}, "
                f"due_date={self.due_date}, priority={self.priority.value}, status={self.status})")
