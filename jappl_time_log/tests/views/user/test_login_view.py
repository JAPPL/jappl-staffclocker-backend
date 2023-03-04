import secrets
from typing import Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestLoginView(APITestCase):
    """Test class for user login."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Mock data for test cases."""
        cls.user: UserDetail = user_instance.make(email="test@gmail.com")
        cls.url = reverse("user:login")

    def test_login_correct_email_and_password(self):
        """Method to test user login successfully."""
        request_body: Dict[str, str] = {"email": self.user.email, "password": self.user.password}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)

    def test_login_incorrect_email_and_password(self):
        """Method to test user login with invalid email or password."""
        request_body: Dict[str, str] = {"email": self.user.email, "password": secrets.token_hex(16)}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_input(self):
        """Method to test user login with invalid request data."""
        response: Response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"email": self.user.email}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"password": secrets.token_hex(16)}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
