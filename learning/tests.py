import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson

User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class CourseAPITests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="test_teacher",
            password="test_password",
        )

    def test_create_course(self):
        data = {
            "title": "Python Course",
            "description": "Test course",
            "teacher": self.teacher.id,
        }

        response = self.client.post(
            "/api/courses/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Course.objects.count(), 1)

        course = Course.objects.first()

        self.assertEqual(course.title, "Python Course")
        self.assertEqual(course.teacher, self.teacher)

    def test_get_courses(self):
        Course.objects.create(
            title="Django Course",
            description="Test",
            teacher=self.teacher,
        )

        response = self.client.get("/api/courses/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(Course.objects.count(), 1)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class LessonFileAPITests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="lesson_teacher",
            password="test_password",
        )

        self.course = Course.objects.create(
            title="Test Course",
            description="Course for tests",
            teacher=self.teacher,
        )

    def test_create_lesson_with_pdf(self):
        pdf_file = SimpleUploadedFile(
            "lesson.pdf",
            b"%PDF-1.4 test pdf content",
            content_type="application/pdf",
        )

        data = {
            "course": self.course.id,
            "title": "Test Lesson",
            "content": "Lesson content",
            "pdf_file": pdf_file,
        }

        response = self.client.post(
            "/api/lessons/",
            data,
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Lesson.objects.count(), 1)

        lesson = Lesson.objects.first()

        self.assertEqual(lesson.title, "Test Lesson")
        self.assertTrue(lesson.pdf_file.name.endswith(".pdf"))

    def test_reject_non_pdf_file(self):
        image_file = SimpleUploadedFile(
            "image.png",
            b"fake image content",
            content_type="image/png",
        )

        data = {
            "course": self.course.id,
            "title": "Invalid File Lesson",
            "content": "Test content",
            "pdf_file": image_file,
        }

        response = self.client.post(
            "/api/lessons/",
            data,
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(Lesson.objects.count(), 0)

    def test_get_lesson(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title="Existing Lesson",
            content="Test content",
        )

        response = self.client.get(f"/api/lessons/{lesson.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Existing Lesson",
        )

    def test_reject_large_pdf(self):
        large_file = SimpleUploadedFile(
            "large.pdf",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="application/pdf",
        )

        data = {
            "course": self.course.id,
            "title": "Large PDF Lesson",
            "content": "Test content",
            "pdf_file": large_file,
        }

        response = self.client.post(
            "/api/lessons/",
            data,
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(Lesson.objects.count(), 0)
