# Online Learning Platform

Платформа онлайн-навчання, розроблена на Python з використанням Django.

Система призначена для створення навчальних курсів і уроків, запису студентів на курси та подальшого відстеження процесу навчання.

## Етап 1. Ініціалізація проєкту та проєктування моделі даних

На першому етапі створено базову структуру застосунку та реалізовано основу для подальшої розробки платформи.

### Виконано

- створено Django-проєкт `config`;
- створено застосунок `learning`;
- налаштовано локальний запуск застосунку;
- реалізовано endpoint `GET /health/`;
- створено основні моделі даних;
- підключено базу даних SQLite;
- створено та застосовано першу міграцію;
- реалізовано Repository layer;
- реалізовано Service layer;
- створено ER-діаграму;
- налаштовано Ruff для перевірки коду;
- налаштовано Black для форматування коду;
- налаштовано використання змінних середовища;
- створено `.env.example`;
- секретні дані виключено з Git за допомогою `.gitignore`.

## Основні сутності

У системі використовуються такі сутності:

### User

Користувач системи. Використовується стандартна модель користувача Django.

### Course

Навчальний курс.

Основні поля:

- `title` — назва курсу;
- `description` — опис;
- `teacher` — викладач;
- `created_at` — дата створення.

### Lesson

Урок, який належить певному курсу.

Основні поля:

- `course` — курс;
- `title` — назва уроку;
- `content` — навчальний матеріал;
- `video_url` — посилання на відео;
- `pdf_file` — PDF-матеріал.

### Enrollment

Запис студента на навчальний курс.

Основні поля:

- `student` — студент;
- `course` — курс;
- `enrolled_at` — дата запису.

Один студент не може бути записаний на один і той самий курс декілька разів.

## Зв'язки між сутностями

Основні зв'язки:

- `User 1:N Course`;
- `Course 1:N Lesson`;
- `User 1:N Enrollment`;
- `Course 1:N Enrollment`.

ER-діаграма знаходиться у файлі:

`ER_DIAGRAM.md`

## Архітектура

У проєкті використовується розділення відповідальностей між шарами.

Архітектура:

`View → Service → Repository → Django ORM → SQLite`

### View

Приймає HTTP-запити та повертає відповіді.

### Service

Містить бізнес-логіку застосунку.

### Repository

Відповідає за роботу з даними через Django ORM.

### ORM

Django ORM використовується для взаємодії з базою даних SQLite.

## Health endpoint

Для перевірки працездатності застосунку реалізовано:

`GET /health/`

При успішній роботі сервер повертає:

```json
{
    "status": "ok",
    "service": "online-learning"
}
```

## Технології

- Python
- Django
- SQLite
- Django ORM
- python-dotenv
- Ruff
- Black
- Git
- GitHub

## Встановлення та запуск

### 1. Клонувати репозиторій

```bash
git clone https://github.com/aradochina2027-sys/online-learning.git
```

### 2. Перейти до папки проєкту

```bash
cd online-learning
```

### 3. Створити віртуальне середовище

```bash
python -m venv venv
```

### 4. Активувати віртуальне середовище

Для Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Встановити залежності

```bash
pip install -r requirements.txt
```

### 6. Створити файл `.env`

У корені проєкту необхідно створити файл:

`.env`

За прикладом файлу:

`.env.example`

Вміст:

```env
DJANGO_SECRET_KEY=your-secret-key-here
```

Замість `your-secret-key-here` необхідно вказати власний секретний ключ Django.

Файл `.env` не додається до Git.

### 7. Застосувати міграції

```bash
python manage.py migrate
```

### 8. Перевірити проєкт

```bash
python manage.py check
```

Очікуваний результат:

```text
System check identified no issues (0 silenced).
```

### 9. Запустити сервер

```bash
python manage.py runserver
```

Після запуску застосунок буде доступний локально.

Для перевірки роботи використовується:

`/health/`

## Перевірка міграцій

Для перевірки міграцій застосунку:

```bash
python manage.py showmigrations learning
```

Міграція повинна бути позначена як виконана:

```text
[X] 0001_initial
```

## Перевірка коду

Перевірка Ruff:

```bash
ruff check .
```

Форматування Black:

```bash
black .
```

Перевірка Django:

```bash
python manage.py check
```

## Структура проєкту

```text
online-learning/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── learning/
│   ├── migrations/
│   ├── repositories/
│   │   └── course_repository.py
│   ├── services/
│   │   └── course_service.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── .env.example
├── .gitignore
├── ER_DIAGRAM.md
├── manage.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Результат Етапу 1

У результаті виконання першого етапу створено базову архітектуру платформи онлайн-навчання.

Застосунок запускається локально, підключено базу даних SQLite, створено основні моделі та міграції, реалізовано Repository і Service шари, ER-діаграму та endpoint для перевірки працездатності застосунку.

Проєкт підготовлений до реалізації наступних етапів.