from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, parsers, viewsets

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Отримати список курсів",
        description=(
            "Повертає список навчальних курсів. "
            "Підтримує фільтрацію за викладачем, пошук, "
            "сортування та пагінацію."
        ),
    ),
    retrieve=extend_schema(
        summary="Отримати курс",
        description="Повертає інформацію про курс за його ID.",
    ),
    create=extend_schema(
        summary="Створити курс",
        description="Створює новий навчальний курс.",
    ),
    update=extend_schema(
        summary="Оновити курс",
        description="Повністю оновлює інформацію про курс.",
    ),
    partial_update=extend_schema(
        summary="Частково оновити курс",
        description="Частково оновлює інформацію про курс.",
    ),
    destroy=extend_schema(
        summary="Видалити курс",
        description="Видаляє навчальний курс за його ID.",
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    queryset = (
        Course.objects.select_related("teacher").prefetch_related("lessons").all()
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "teacher",
    ]

    search_fields = [
        "title",
        "description",
        "teacher__username",
    ]

    ordering_fields = [
        "id",
        "title",
        "created_at",
    ]

    ordering = [
        "id",
    ]


@extend_schema_view(
    list=extend_schema(
        summary="Отримати список уроків",
        description=(
            "Повертає список уроків. "
            "Підтримує фільтрацію за курсом, пошук, "
            "сортування та пагінацію."
        ),
    ),
    retrieve=extend_schema(
        summary="Отримати урок",
        description="Повертає інформацію про урок за його ID.",
    ),
    create=extend_schema(
        summary="Створити урок",
        description=(
            "Створює новий урок для навчального курсу. "
            "Підтримує завантаження PDF-файлу."
        ),
    ),
    update=extend_schema(
        summary="Оновити урок",
        description=(
            "Повністю оновлює інформацію про урок. " "Підтримує завантаження PDF-файлу."
        ),
    ),
    partial_update=extend_schema(
        summary="Частково оновити урок",
        description=(
            "Частково оновлює інформацію про урок. " "Підтримує завантаження PDF-файлу."
        ),
    ),
    destroy=extend_schema(
        summary="Видалити урок",
        description="Видаляє урок за його ID.",
    ),
)
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    parser_classes = [
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser,
    ]

    queryset = Lesson.objects.select_related("course", "course__teacher").all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "course",
    ]

    search_fields = [
        "title",
        "content",
    ]

    ordering_fields = [
        "id",
        "title",
    ]

    ordering = [
        "id",
    ]
