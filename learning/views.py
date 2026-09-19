from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    queryset = (
        Course.objects
        .select_related("teacher")
        .prefetch_related("lessons")
        .all()
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


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    queryset = (
        Lesson.objects
        .select_related("course", "course__teacher")
        .all()
    )

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