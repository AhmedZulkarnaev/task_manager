import typer
from rich.console import Console
from rich.table import Table
from models import Task
from database import insert_task, get_tasks

console = Console()
app = typer.Typer()


@app.command(short_help="Добавление задачи")
def add(title: str, description: str, category: str, priority: str = "средний"):
    """Добавление новой задачи."""
    typer.echo(f"Добавление задачи: {title}, {description}, {category}, {priority}")
    task = Task(title, description, category, priority)
    insert_task(task)
    show()


@app.command()
def show():
    tasks = get_tasks()
    console.print("[bold magenta]TaskManager[/bold magenta]")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Задача", min_width=20)
    table.add_column("Описание", min_width=20)
    table.add_column("Категория", min_width=15, justify="right")
    table.add_column("Статус", min_width=15, justify="right")
    table.add_column("Дата добавления", min_width=20)

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'YouTube': 'red', 'Sports': 'cyan', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(idx), task.title, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)


if __name__ == "__main__":
    app()