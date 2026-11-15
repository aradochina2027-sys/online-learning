from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .auth_views import current_user, logout_user, register_user
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
    # JWT-автентифікація
    path(
        "auth/register/",
        register_user,
        name="auth-register",
    ),
    path(
        "auth/login/",
        TokenObtainPairView.as_view(),
        name="auth-login",
    ),
    path(
        "auth/refresh/",
        TokenRefreshView.as_view(),
        name="auth-refresh",
    ),
    path(
        "auth/logout/",
        logout_user,
        name="auth-logout",
    ),
    path(
        "auth/me/",
        current_user,
        name="auth-me",
    ),
    # Фонові задачі
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
    # Зовнішній REST API
    path(
        "external/posts/",
        external_posts,
        name="external-posts",
    ),
    # Курси та уроки
    path("", include(router.urls)),
]
