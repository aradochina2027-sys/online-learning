from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Course, Lesson


User = get_user_model()


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