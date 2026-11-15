from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.username = "jwt_test_student"
        self.password = "SecureStudy2026!Test"

        self.user = User.objects.create_user(
            username=self.username,
            email="jwt@example.com",
            password=self.password,
        )

    def login(self):
        return self.client.post(
            "/api/auth/login/",
            {
                "username": self.username,
                "password": self.password,
            },
            format="json",
        )

    def test_registration_hashes_password(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "new_student",
                "email": "new@example.com",
                "password": "StrongPassword2026!Test",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(username="new_student")
        self.assertTrue(user.check_password("StrongPassword2026!Test"))
        self.assertNotEqual(
            user.password,
            "StrongPassword2026!Test",
        )

    def test_duplicate_registration_rejected(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": self.username,
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_returns_access_and_refresh(self):
        response = self.login()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_password_rejected(self):
        response = self.client.post(
            "/api/auth/login/",
            {
                "username": self.username,
                "password": "WrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_protected_endpoint_without_token(self):
        response = self.client.get("/api/auth/me/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_protected_endpoint_with_token(self):
        tokens = self.login().data

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        response = self.client.get("/api/auth/me/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["username"],
            self.username,
        )

    def test_refresh_returns_new_tokens(self):
        tokens = self.login().data

        response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": tokens["refresh"]},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_logout_blacklists_refresh(self):
        tokens = self.login().data

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        logout_response = self.client.post(
            "/api/auth/logout/",
            {"refresh": tokens["refresh"]},
            format="json",
        )

        self.assertEqual(
            logout_response.status_code,
            status.HTTP_200_OK,
        )

        refresh_response = self.client.post(
            "/api/auth/refresh/",
            {"refresh": tokens["refresh"]},
            format="json",
        )

        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_course_creation_requires_jwt(self):
        response = self.client.post(
            "/api/courses/",
            {
                "title": "Protected Course",
                "description": "JWT test",
                "teacher": self.user.pk,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_lesson_creation_requires_jwt(self):
        response = self.client.post(
            "/api/lessons/",
            {
                "title": "Protected Lesson",
                "content": "JWT test",
                "course": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_background_task_requires_jwt(self):
        response = self.client.post("/api/tasks/reports/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
