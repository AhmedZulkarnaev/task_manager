from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from database import insert_task, get_tasks, delete_task, update_task
from models import Priority

from save_data import save_tasks_to_json
from validators import date_type

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
    if not title or not description or not category:
        typer.echo("Ошибка: Название, описание и категория не могут быть пустыми.")
        raise typer.Exit(code=1)

    if due_date:
        date_type(due_date)

    typer.echo(f"Добавление задачи: {title}, {description}, {category}, {priority.value}")
    task = Task(title, description, category, priority, due_date=due_date)
    insert_task(task)
    show()


@app.command(short_help="Удаление задачи")
def delete(task_id: Optional[int] = None, category: Optional[str] = None):
    """Удаляет задачи."""
    if task_id is None and category is None:
        typer.echo("Ошибка: Необходимо указать task_id или category для удаления задачи.")
        raise typer.Exit(code=1)
    delete_task(task_id, category)
    show()


@app.command(short_help="Редактирование задачи")
def update(
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None
):
    """Команда для редактирования задачи"""
    if due_date:
        date_type(due_date)

    if status and status not in ["Не выполнена", "В процессе", "Выполнена"]:
        typer.echo("Недопустимый статус. Допустимые значения: 'Не выполнена', 'В процессе', 'Выполнена'.")
        raise typer.Exit(code=1)

    update_task(
        task_id,
        title=title,
        description=description,
        due_date=due_date,
        status=status
    )
    show()


@app.command(short_help="Вывод таблицы с задачами")
def show(category: Optional[str] = None, status: Optional[str] = None):
    tasks = get_tasks(category=category, status=status)
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
        table.add_row(
            str(idx),
            task.title,
            task.description,
            f'[{c}]{task.category}[/{c}]',
            str(task.due_date),
            task.priority,
            task.status,
        )
    console.print(table)
    save_tasks_to_json(tasks, "tasks.json")


if __name__ == "__main__":
    app()
