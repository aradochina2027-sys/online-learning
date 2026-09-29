from pathlib import Path

from django.conf import settings
from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson

        fields = [
            "id",
            "course",
            "title",
            "content",
            "video_url",
            "pdf_file",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Назва уроку повинна містити мінімум 3 символи."
            )

        return value

    def validate_pdf_file(self, value):
        if not value:
            return value

        # Перевірка розміру файлу
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(
                "Розмір PDF-файлу не повинен перевищувати 5 МБ."
            )

        # Перевірка розширення файлу
        extension = Path(value.name).suffix.lower()

        if extension != ".pdf":
            raise serializers.ValidationError(
                "Дозволено завантажувати тільки PDF-файли."
            )

        # Перевірка MIME-типу
        content_type = getattr(value, "content_type", None)

        if content_type and content_type != "application/pdf":
            raise serializers.ValidationError("Файл повинен мати тип application/pdf.")

        return value


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(
        many=True,
        read_only=True,
    )

    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True,
    )

    class Meta:
        model = Course

        fields = [
            "id",
            "title",
            "description",
            "teacher",
            "teacher_name",
            "created_at",
            "lessons",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "teacher_name",
            "lessons",
        ]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Назва курсу повинна містити мінімум 3 символи."
            )

        return value
