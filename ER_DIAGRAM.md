# ER-діаграма платформи онлайн-навчання

┌─────────────────┐
│      USER       │
├─────────────────┤
│ id              │
│ username        │
│ email           │
└───────┬─────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│     COURSE      │
├─────────────────┤
│ id              │
│ title           │
│ description     │
│ teacher_id (FK) │
│ created_at      │
└───────┬─────────┘
        │
        │ 1:N
        ▼
┌─────────────────┐
│     LESSON      │
├─────────────────┤
│ id              │
│ course_id (FK)  │
│ title           │
│ content         │
│ video_url       │
│ pdf_file        │
└─────────────────┘


┌─────────────────┐
│      USER       │
└───────┬─────────┘
        │ 1:N
        ▼
┌─────────────────┐
│   ENROLLMENT    │
├─────────────────┤
│ id              │
│ student_id (FK) │
│ course_id (FK)  │
│ enrolled_at     │
└───────┬─────────┘
        │ N:1
        ▼
┌─────────────────┐
│     COURSE      │
└─────────────────┘
Зв'язки:

User 1:N Course
Course 1:N Lesson
User 1:N Enrollment
Course 1:N Enrollment