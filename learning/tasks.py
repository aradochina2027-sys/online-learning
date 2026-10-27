import logging
from concurrent.futures import ThreadPoolExecutor

from django.db import close_old_connections
from django.utils import timezone

from .models import BackgroundTask, Course

logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=2)


def generate_courses_report(task_id):
    close_old_connections()

    try:
        BackgroundTask.objects.filter(id=task_id).update(
            status=BackgroundTask.Status.RUNNING,
            started_at=timezone.now(),
        )

        courses = Course.objects.select_related("teacher").prefetch_related(
            "lessons", "enrollments"
        )

        report = []

        for course in courses:
            report.append(
                {
                    "id": course.id,
                    "title": course.title,
                    "teacher": course.teacher.username,
                    "lessons_count": len(course.lessons.all()),
                    "students_count": len(course.enrollments.all()),
                }
            )

        result = {
            "total_courses": len(report),
            "courses": report,
        }

        BackgroundTask.objects.filter(id=task_id).update(
            status=BackgroundTask.Status.COMPLETED,
            result=result,
            finished_at=timezone.now(),
        )

    except Exception:
        logger.exception("Помилка генерації звіту для задачі %s", task_id)

        BackgroundTask.objects.filter(id=task_id).update(
            status=BackgroundTask.Status.FAILED,
            error="Не вдалося згенерувати звіт.",
            finished_at=timezone.now(),
        )

    finally:
        close_old_connections()


def start_courses_report():
    task = BackgroundTask.objects.create()

    try:
        executor.submit(generate_courses_report, task.id)
    except RuntimeError:
        task.status = BackgroundTask.Status.FAILED
        task.error = "Фоновий виконавець недоступний."
        task.finished_at = timezone.now()
        task.save(update_fields=["status", "error", "finished_at"])

    return task
