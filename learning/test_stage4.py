from unittest.mock import Mock, patch

import requests
from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .external_api import ExternalAPIError, get_external_posts
from .models import BackgroundTask


class BackgroundTaskAPITests(APITestCase):
    @patch("learning.views.start_courses_report")
    def test_create_background_task_returns_202(self, mock_start):
        task = Mock()
        task.id = "123e4567-e89b-12d3-a456-426614174000"
        task.status = BackgroundTask.Status.PENDING
        mock_start.return_value = task

        response = self.client.post("/api/tasks/reports/")

        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED,
        )
        mock_start.assert_called_once()

    def test_get_background_task(self):
        task = BackgroundTask.objects.create(
            status=BackgroundTask.Status.COMPLETED,
            result={"total_courses": 0, "courses": []},
        )

        response = self.client.get(f"/api/tasks/{task.id}/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["status"],
            BackgroundTask.Status.COMPLETED,
        )

    def test_get_nonexistent_task(self):
        response = self.client.get("/api/tasks/123e4567-e89b-12d3-a456-426614174000/")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class ExternalAPITests(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    @patch("learning.external_api.requests.get")
    def test_external_api_success(self, mock_get):
        response = Mock()
        response.json.return_value = [{"id": 1, "title": "Test post"}]
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        result = get_external_posts()

        self.assertEqual(result["source"], "external_api")
        self.assertEqual(len(result["data"]), 1)
        mock_get.assert_called_once()

    @patch("learning.external_api.requests.get")
    def test_external_api_cache(self, mock_get):
        response = Mock()
        response.json.return_value = [{"id": 1, "title": "Cached post"}]
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        first_result = get_external_posts()
        second_result = get_external_posts()

        self.assertEqual(first_result["source"], "external_api")
        self.assertEqual(second_result["source"], "cache")
        mock_get.assert_called_once()

    @patch("learning.external_api.requests.get")
    def test_external_api_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout()

        with self.assertRaises(ExternalAPIError):
            get_external_posts()

    @patch("learning.external_api.requests.get")
    def test_external_api_network_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError()

        with self.assertRaises(ExternalAPIError):
            get_external_posts()

    @patch("learning.external_api.requests.get")
    def test_external_api_invalid_json(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = response

        with self.assertRaises(ExternalAPIError):
            get_external_posts()

    @patch("learning.external_api.requests.get")
    @override_settings(EXTERNAL_API_TIMEOUT=3)
    def test_external_api_uses_timeout(self, mock_get):
        response = Mock()
        response.json.return_value = []
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        get_external_posts()

        self.assertEqual(
            mock_get.call_args.kwargs["timeout"],
            3,
        )


class BackgroundTaskNonBlockingTests(APITestCase):
    @patch("learning.tasks.executor.submit")
    def test_background_task_does_not_wait_for_completion(self, mock_submit):
        response = self.client.post("/api/tasks/reports/")

        self.assertEqual(
            response.status_code,
            status.HTTP_202_ACCEPTED,
        )

        self.assertEqual(
            BackgroundTask.objects.count(),
            1,
        )

        task = BackgroundTask.objects.first()

        self.assertEqual(
            task.status,
            BackgroundTask.Status.PENDING,
        )

        mock_submit.assert_called_once()
