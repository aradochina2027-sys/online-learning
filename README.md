# Online Learning Platform

Платформа онлайн-навчання, розроблена на Python та Django.

## Основні можливості

- створення курсів;
- створення уроків;
- запис студентів на курси;
- збереження навчальних матеріалів;
- робота з базою даних.

## Основні сутності

- User
- Course
- Lesson
- Enrollment

## Технології

- Python
- Django
- SQLite
- Django ORM
- Black
- Ruff

## Архітектура

View → Service → Repository → Django ORM → SQLite

## Запуск проєкту

Створити та активувати віртуальне середовище.

Встановити залежності:

pip install -r requirements.txt

Виконати міграції:

python manage.py migrate

Запустити сервер:

python manage.py runserver

## Health endpoint

GET /health/

Результат:

{"status": "ok", "service": "online-learning"}