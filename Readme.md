# Task Manager

Task Manager - это приложение для управления задачами, которое позволяет создавать, редактировать, удалять и сохранять задачи в формате JSON.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/AhmedZulkarnaev/task_manager/blob/master/models.py

2. Перейдите в директорию проекта:

    ```bash
   cd task-manager

3. Активируйте виртуальное окружение и установите зависимости из файла requirements.txt
    ```bash
   Windows - env/Scripts/activate
   Linux/MacOS - source env/bin/activate
   
   #установка зависимостей
   pip install -r requirements.txt
   ```

4. Все команды исполняются файлом cli_app.py
    ```bash
    #Все команды с описанием доступны по команде
    ----> python cli_app.py --help <----
    #Примеры использования
    python cli_app.py update --task_id 1 --title "Новое название" --status "Выполнена" (редактирование задачи)
    python cli_app.py show (Вывод таблицы с задачами)
   ```
 

### ВНИМАНИЕ!
Задачи автоматически сохраняются в json файле.

Проект требует доработок.

Код тестами не покрыт.



