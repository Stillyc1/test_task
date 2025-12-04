.PHONY: install run migrate test worker lint

# Установка зависимостей
install:
	poetry install

# Запуск Django-сервера
run:
	poetry run python manage.py runserver 0.0.0.0:8000

# Применение миграций
migrate:
	poetry run python manage.py migrate

# Запуск тестов
test:
	poetry run python manage.py test

# Запуск Celery worker
worker:
	poetry run celery -A config worker -l INFO -P eventlet

# Проверка кода через Flake8
lint:
	poetry run flake8 .

# Запуск всех сервисов через Docker Compose
up:
	docker-compose up --build

# Остановка всех сервисов
down:
	docker-compose down

# Пересборка и запуск с удалением томов (чистый запуск)
rebuild:
	docker-compose down --volumes --remove-orphans
	docker-compose up --build --force-recreate