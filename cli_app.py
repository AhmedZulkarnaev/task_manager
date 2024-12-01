import typer
from rich.console import Console
from rich.table import Table
from models import Task, Priority
from database import insert_task, get_tasks, delete_task, update_task
from typing import Optional

from test import date_type

console = Console()
app = typer.Typer()


@app.command(short_help="Добавление задачи")
def add(
        title: str,
        description: str,
        category: str,
        due_date: Optional[str] = None,
        priority: Priority = "средний"):
    """Добавление новой задачи."""
    if due_date:
        due_date = date_type(due_date)
    typer.echo(f"Добавление задачи: {title}, {description}, {category}, {priority.value}")
    task = Task(title, description, category, priority, due_date=due_date)
    insert_task(task)
    show()


@app.command(short_help="Удаление задачи")
def delete(task_id: Optional[int] = None, category: Optional[str] = None):
    """Удаляет задачи."""
    delete_task(task_id, category)
    show()


@app.command(short_help="Редактирование задачи")
def update(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    status: Optional[int] = None
):
    """Команда для редактирования задачи"""
    update_task(
        task_id,
        title=title,
        description=description,
        due_date=due_date,
        status=status
    )
    show()


@app.command(short_help="Вывод таблицы с задачами")
def show():
    tasks = get_tasks()
    console.print("[bold magenta]TaskManager[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6, justify="center")
    table.add_column("Название", min_width=20, justify="center")
    table.add_column("Описание", min_width=20, justify="center")
    table.add_column("Категория", min_width=15, justify="center")
    table.add_column("Срок выполнения", min_width=20, justify="center")
    table.add_column("Приоритет", min_width=15, justify="center")
    table.add_column("Статус", min_width=15, justify="center")

    def get_category_color(category):
        colors = {'Обучение': 'cyan', 'Личное': 'red', 'Работа': 'cyan'}
        return colors.get(category, 'white')

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "Выполнено" if task.status == "2" else "Не выполнено"
        table.add_row(
            str(idx),
            task.title,
            task.description,
            f'[{c}]{task.category}[/{c}]',
            str(task.due_date),
            task.priority,
            is_done_str,
        )
    console.print(table)


if __name__ == "__main__":
    app()
