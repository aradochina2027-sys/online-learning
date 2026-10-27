import sqlite3
import statistics
import tempfile
import time
from pathlib import Path

TOTAL_COURSES = 50_000
REPEAT_COUNT = 300
SEARCH_TITLE = "Python Course 25000"


def measure_query(cursor):
    measurements = []

    for _ in range(REPEAT_COUNT):
        start = time.perf_counter()

        cursor.execute(
            "SELECT * FROM courses WHERE title = ?",
            (SEARCH_TITLE,),
        )
        cursor.fetchall()

        elapsed = (time.perf_counter() - start) * 1000
        measurements.append(elapsed)

    return statistics.median(measurements)


def show_query_plan(cursor):
    cursor.execute(
        "EXPLAIN QUERY PLAN " "SELECT * FROM courses WHERE title = ?",
        (SEARCH_TITLE,),
    )

    for row in cursor.fetchall():
        print(row[3])


def main():
    with tempfile.TemporaryDirectory() as directory:
        database_path = Path(directory) / "benchmark.sqlite3"

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        try:
            cursor.execute("""
                CREATE TABLE courses (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL
                )
                """)

            print(f"Створюємо {TOTAL_COURSES} тестових курсів...")

            cursor.executemany(
                """
                INSERT INTO courses (title, description)
                VALUES (?, ?)
                """,
                (
                    (f"Python Course {i}", "Test description")
                    for i in range(TOTAL_COURSES)
                ),
            )

            connection.commit()

            print("\n=== ДО ОПТИМІЗАЦІЇ ===")
            show_query_plan(cursor)

            before = measure_query(cursor)
            print(f"Медіанний час пошуку: {before:.4f} мс")

            cursor.execute("CREATE INDEX idx_courses_title ON courses(title)")
            connection.commit()

            print("\n=== ПІСЛЯ ОПТИМІЗАЦІЇ ===")
            show_query_plan(cursor)

            after = measure_query(cursor)
            print(f"Медіанний час пошуку: {after:.4f} мс")

            if after > 0:
                acceleration = before / after
                improvement = (before - after) / before * 100

                print("\n=== РЕЗУЛЬТАТ ===")
                print(f"Прискорення: {acceleration:.2f} разів")
                print(f"Скорочення часу: {improvement:.2f}%")

        finally:
            connection.close()


if __name__ == "__main__":
    main()
