# Online Learning Platform

Платформа онлайн-навчання, розроблена на Python та Django.

## Основні можливості

- створення та керування навчальними курсами;
- створення та керування уроками;
- запис студентів на курси;
- збереження навчальних матеріалів;
- REST API для роботи з курсами та уроками;
- фільтрація, пошук, сортування та пагінація;
- завантаження PDF-файлів до уроків;
- перевірка типу та розміру завантажених файлів;
- OpenAPI-документація;
- інтерактивна документація Swagger UI;
- інтеграційне тестування API.

## Основні сутності

- User
- Course
- Lesson
- Enrollment

## Технології

- Python
- Django
- Django REST Framework
- Django Filter
- drf-spectacular
- SQLite
- Django ORM
- OpenAPI / Swagger
- Black
- Ruff

## Архітектура

Основна структура застосунку:

```text
View → Service → Repository → Django ORM → SQLite
```

REST API використовує Django REST Framework.

## Встановлення

Створити віртуальне середовище:

```powershell
python -m venv venv
```

Активувати його у PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Встановити залежності:

```powershell
pip install -r requirements.txt
```

## База даних

Виконати міграції:

```powershell
python manage.py migrate
```

## Запуск проєкту

Запустити сервер:

```powershell
python manage.py runserver
```

Після запуску застосунок доступний за адресою:

```text
http://127.0.0.1:8000/
```

## REST API

Основні endpoints:

```text
GET    /api/courses/
POST   /api/courses/
GET    /api/courses/{id}/
PUT    /api/courses/{id}/
PATCH  /api/courses/{id}/
DELETE /api/courses/{id}/

GET    /api/lessons/
POST   /api/lessons/
GET    /api/lessons/{id}/
PUT    /api/lessons/{id}/
PATCH  /api/lessons/{id}/
DELETE /api/lessons/{id}/
```

API підтримує:

- фільтрацію;
- пошук;
- сортування;
- пагінацію;
- єдиний формат обробки помилок.

## OpenAPI та Swagger

OpenAPI-схема:

```text
http://127.0.0.1:8000/api/schema/
```

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

Swagger UI дозволяє переглядати документацію та виконувати API-запити безпосередньо з браузера.

## Робота з файлами

До уроку можна завантажити PDF-файл через поле:

```text
pdf_file
```

Для завантаження файлів використовується:

```text
multipart/form-data
```

Обмеження:

- дозволено тільки PDF;
- MIME-тип: `application/pdf`;
- максимальний розмір файлу — 5 МБ.

Завантажені файли зберігаються у каталозі:

```text
media/lessons/
```

У режимі розробки файли доступні через:

```text
/media/
```

## Інтеграційні тести

Проєкт містить інтеграційні тести API.

Перевіряються:

- створення курсу;
- отримання курсів;
- створення уроку з PDF;
- отримання уроку;
- відхилення файлу неправильного типу;
- відхилення PDF-файлу розміром понад 5 МБ;
- зміни стану бази даних після API-запитів.

Запуск тестів:

```powershell
python manage.py test learning
```

Під час тестування Django автоматично створює окрему тестову базу даних та видаляє її після завершення тестів.

На Етапі 3 реалізовано 6 інтеграційних тестів.

## Перевірка коду

Перевірка Django:

```powershell
python manage.py check
```

Форматування:

```powershell
black .
```

Статичний аналіз:

```powershell
ruff check .
```

## Етап 1

Реалізовано:

- базову структуру Django-проєкту;
- моделі даних;
- SQLite;
- першу міграцію;
- Repository та Service layers;
- health endpoint;
- ER-діаграму;
- Black та Ruff.

## Етап 2

Реалізовано:

- REST API;
- CRUD для Course;
- CRUD для Lesson;
- серіалізатори;
- валідацію даних;
- фільтрацію;
- пошук;
- сортування;
- пагінацію;
- обробку API-помилок.

## Етап 3

Реалізовано:

- OpenAPI-специфікацію;
- Swagger UI;
- описи основних endpoints;
- завантаження PDF-файлів;
- перевірку типу файлу;
- обмеження розміру файлу до 5 МБ;
- повернення посилання на завантажений файл клієнту;
- інтеграційні тести;
- окрему тестову базу даних.

## Health endpoint

```text
GET /health/
```

Очікувана відповідь:

```json
{
  "status": "ok",
  "service": "online-learning"
}
```