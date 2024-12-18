# Это бэкенд-часть для трекера полезных привычек, реализованного с использованием Django и Django REST Framework (DRF). Проект создан как часть курсовой работы по разработке SPA веб-приложения для отслеживания привычек.
Инструкции по запуску
команды для установки на Linux:

sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo apt install docker-compose

Эта команда соберет Docker образы и запустит все сервисы.

Склонируйте репозиторий проекта

Настройка переменных окружения

Запустите сборку и все необходимые сервисы:

docker-compose up --build

Выполнение миграций базы данных:

docker-compose exec django python manage.py migrat

Доступ к приложению:

http://localhost:8000

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/ваш_аккаунт/habit_tracker.git

Установите зависимости с помощью Poetry:
poetry install

Создайте файл .env для переменных окружения см. файл .env.sample

Выполните миграции базы данных:
poetry run python manage.py migrate

Создайте суперпользователя:
poetry run python manage.py createsuperuser

Запуск проекта

Запустите сервер разработки Django:
poetry run python manage.py runserver

Запустите Celery для выполнения отложенных задач:
poetry run celery -A config worker --loglevel=INFO

Запустите Celery Beat для периодических задач:
poetry run celery -A config beat --loglevel=INFO

Тестирование
Проект покрыт тестами. Для запуска тестов выполните команду:
poetry run python manage.py test

Также в проекте настроена проверка покрытия тестами с использованием coverage. Для запуска покрытия тестов выполните:
poetry run coverage run --source='.' manage.py test
poetry run coverage report