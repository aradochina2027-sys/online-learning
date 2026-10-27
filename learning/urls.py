from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .external_views import external_posts
from .views import (
    CourseViewSet,
    LessonViewSet,
    create_courses_report,
    get_background_task,
)

router = DefaultRouter()

router.register(
    r"courses",
    CourseViewSet,
    basename="course",
)

router.register(
    r"lessons",
    LessonViewSet,
    basename="lesson",
)


urlpatterns = [
    path(
        "tasks/reports/",
        create_courses_report,
        name="create-courses-report",
    ),
    path(
        "tasks/<uuid:task_id>/",
        get_background_task,
        name="get-background-task",
    ),
    path(
        "external/posts/",
        external_posts,
        name="external-posts",
    ),
    path("", include(router.urls)),
]
