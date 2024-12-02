import datetime

import typer


def date_type(value: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise typer.BadParameter("Неверный формат даты. Используйте формат YYYY-MM-DD.")
