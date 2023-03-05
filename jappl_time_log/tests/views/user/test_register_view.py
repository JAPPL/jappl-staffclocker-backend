import secrets
from typing import Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.services.user.user_account_service import UserAccountService
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestLoginView(APITestCase):
    """Test class for user registration."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Mock data for test cases."""
        raw_password = secrets.token_hex(16)
        hashed_password = UserAccountService.hash_password(raw_password)
        cls.user: UserDetail = user_instance.make(email="test@gmail.com", password=hashed_password)
        cls.raw_password: str = raw_password
        cls.url = reverse("user:register")

    def test_register_successfully(self) -> None:
        """Method to test user register successfully."""
        request_body: Dict[str, str] = {
            "email": "test2@gmail.com",
            "password": self.raw_password,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_email(self) -> None:
        """Method to test user register with duplicate email."""
        request_body: Dict[str, str] = {
            "email": self.user.email,
            "password": self.raw_password,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_register_invalid_input(self) -> None:
        """Method to test user register with invalid request data."""
        response: Response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"email": self.user.email, "password": secrets.token_hex(16)}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"password": secrets.token_hex(16)}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"email": self.user.email}
        response: Response = self.client.post(self.url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
