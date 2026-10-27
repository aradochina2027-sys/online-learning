
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
- перевірка типу та розміру файлів;
- OpenAPI-документація та Swagger UI;
- інтеграційне тестування API;
- налаштування development і production через змінні середовища;
- асинхронний запуск фонових задач;
- інтеграція із зовнішнім REST API;
- кешування зовнішніх запитів;
- обробка мережевих помилок і тайм-аутів;
- оптимізація запитів SQLite за допомогою індексів.

## Основні сутності

- User
- Course
- Lesson
- Enrollment
- BackgroundTask

## Технології

- Python
- Django
- Django REST Framework
- Django Filter
- drf-spectacular
- SQLite
- Django ORM
- Requests
- Django Cache Framework
- ThreadPoolExecutor
- OpenAPI / Swagger
- Black
- Ruff

## Архітектура

Основна структура застосунку:

```text
View → Service → Repository → Django ORM → SQLite
```

REST API використовує Django REST Framework.

Для фонових задач використовується ThreadPoolExecutor.
Статус і результати задач зберігаються в базі даних.

Для зовнішньої інтеграції використовується бібліотека Requests.
Кешування реалізовано засобами Django.

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
python -m pip install -r requirements.txt
```

## Налаштування середовища

Проєкт використовує файл `.env` для конфігурації.

Створити `.env` на основі прикладу:

```powershell
Copy-Item .env.example .env
```

Відкрити `.env` та встановити власний секретний ключ Django.

Приклад конфігурації для розробки:

```dotenv
DJANGO_ENV=development
DJANGO_DEBUG=true
DJANGO_SECRET_KEY=replace-with-your-own-secret-key
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

EXTERNAL_API_URL=https://jsonplaceholder.typicode.com
EXTERNAL_API_TIMEOUT=5
EXTERNAL_API_CACHE_TIMEOUT=300

DJANGO_SECURE_SSL_REDIRECT=true
```

Згенерувати секретний ключ можна командою:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Значення `DJANGO_SECRET_KEY` потрібно замінити на згенерований ключ.

Файл `.env` не можна завантажувати до GitHub, оскільки він містить секретні налаштування.

### Development

```dotenv
DJANGO_ENV=development
DJANGO_DEBUG=true
```

### Production

```dotenv
DJANGO_ENV=production
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=example.com
DJANGO_SECURE_SSL_REDIRECT=true
```

Для production необхідно встановити справжній домен, надійний секретний ключ та налаштувати HTTPS.

Параметри захищених cookie застосовуються в production. Наведена конфігурація не є повною інструкцією з розгортання: для реального сервера також потрібні налаштування вебсервера, HTTPS, статичних файлів та зберігання даних.

## База даних

Виконати міграції:

```powershell
python manage.py migrate
```

Перевірити стан міграцій:

```powershell
python manage.py makemigrations --check --dry-run
```

## Запуск проєкту

Запустити сервер:

```powershell
python manage.py runserver
```

Адреса локального сервера:

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
- обробку помилок.

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

Завантажені файли зберігаються в каталозі:

```text
media/lessons/
```

У режимі розробки файли доступні через:

```text
/media/
```

## Фонові задачі

Для запуску фонової генерації звіту про курси використовується:

```text
POST /api/tasks/reports/
```

Приклад відповіді:

```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending"
}
```

HTTP-відповідь повертається зі статусом:

```text
202 Accepted
```

Отримання статусу та результату задачі:

```text
GET /api/tasks/{task_id}/
```

Можливі стани задачі:

- `pending` — очікує виконання;
- `running` — виконується;
- `completed` — завершена;
- `failed` — помилка.

Звіт містить кількість курсів, їхні назви, викладачів, кількість уроків і записаних студентів.

Фонові задачі реалізовані за допомогою `ThreadPoolExecutor` без зовнішнього брокера повідомлень.

Обмеження: такий механізм призначений для навчального проєкту. Він не гарантує виконання задач після перезапуску процесу сервера.

## Зовнішній REST API

Для інтеграції використовується тестовий сервіс JSONPlaceholder:

```text
https://jsonplaceholder.typicode.com
```

Отримання публікацій:

```text
GET /api/external/posts/
```

При успішному запиті повертається HTTP 200.

Джерело даних позначається полем `source`:

- `external_api` — дані отримано із зовнішнього сервісу;
- `cache` — дані отримано з кешу.

Після першого успішного запиту результат зберігається в кеші Django.

Час кешування задається змінною:

```dotenv
EXTERNAL_API_CACHE_TIMEOUT=300
```

Тайм-аут HTTP-запиту:

```dotenv
EXTERNAL_API_TIMEOUT=5
```

Передбачено обробку:

- мережевих помилок;
- тайм-аутів;
- HTTP-помилок зовнішнього сервісу;
- некоректного JSON;
- некоректного формату відповіді.

Якщо зовнішній сервіс недоступний і потрібних даних немає в кеші, API повертає HTTP 503.

Для кешування використовується `LocMemCache`. Кеш зберігається в пам'яті процесу та очищується після його перезапуску.

## Оптимізація бази даних

Проведено аналіз запиту пошуку курсу за назвою:

```sql
SELECT * FROM learning_course WHERE title = 'Python';
```

До оптимізації план запиту містив:

```text
SCAN learning_course
```

Це означає повний перегляд таблиці.

До моделі `Course` додано індекс поля `title`:

```python
class Meta:
    indexes = [
        models.Index(
            fields=["title"],
            name="idx_course_title",
        ),
    ]
```

Індекс створено міграцією:

```text
learning/migrations/0003_course_idx_course_title.py
```

Після створення індексу перевірка його використання показала:

```text
SEARCH learning_course USING INDEX idx_course_title (title=?)
```

### Вимірювання продуктивності

Для коректного порівняння створено окрему тимчасову SQLite-базу з 50 000 тестових курсів.

Скрипт:

```powershell
python benchmark_indexes.py
```

Результати тестування:

| Показник | До оптимізації | Після оптимізації |
|---|---|---|
| План виконання | SCAN | SEARCH USING INDEX |
| Медіанний час пошуку | 6,6800 мс | 0,0717 мс |
| Прискорення | — | 93,23 раза |
| Скорочення часу | — | 98,93% |

Час вимірювався на тестовій базі, а не на основній базі проєкту.

Результати залежать від комп'ютера та навантаження системи.

## Автоматичні тести

У проєкті реалізовано 16 тестів:

- 6 тестів попередніх етапів;
- 10 тестів Етапу 4.

Перевіряються:

- створення курсу;
- отримання курсів;
- створення уроку з PDF;
- отримання уроку;
- відхилення неправильного типу файлу;
- відхилення PDF понад 5 МБ;
- запуск фонової задачі;
- отримання статусу задачі;
- обробка неіснуючої задачі;
- передавання задачі фоновому виконавцю без очікування її завершення;
- успішний зовнішній API-запит;
- використання кешу;
- мережеві помилки;
- тайм-аути;
- некоректний JSON;
- налаштування тайм-ауту.

Запуск усіх тестів:

```powershell
python manage.py test learning
```

Під час тестування Django створює окрему тестову базу даних і видаляє її після завершення.

Останній результат:

```text
Found 16 test(s).
Ran 16 tests in 6.120s

OK
```

## Перевірка коду

Перевірка Django:

```powershell
python manage.py check
```

Перевірка форматування:

```powershell
python -m black --check .
```

Автоматичне форматування:

```powershell
python -m black .
```

Статичний аналіз:

```powershell
ruff check .
```

Перевірка залежностей:

```powershell
python -m pip check
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
- повернення посилання на завантажений файл;
- інтеграційні тести;
- окрему тестову базу даних.

## Етап 4

Реалізовано:

- розділення development і production конфігурацій;
- використання змінних середовища;
- зберігання секретного ключа поза кодом;
- фонові задачі без зовнішнього брокера;
- API запуску задач і перевірки результатів;
- зовнішню REST-інтеграцію;
- кешування відповідей;
- обробку мережевих помилок і тайм-аутів;
- аналіз SQL-запитів через EXPLAIN QUERY PLAN;
- створення індексу для пошуку курсів;
- вимірювання продуктивності до та після оптимізації;
- автоматичні тести нової функціональності.

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
