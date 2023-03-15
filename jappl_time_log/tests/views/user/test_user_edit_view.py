import json
import secrets
from typing import Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.user.user_edit_serializer import UserEditSerializer
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestUserEditView(APITestCase):
    """Test class for edit user information."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for edit user test cases."""
        user: UserDetail = user_instance.make(email="test.edit@gmail.com")
        cls.token: str = "Bearer " + str(RefreshToken.for_user(user=user).access_token)
        cls.first_name: str = secrets.token_hex(16)
        cls.last_name: str = secrets.token_hex(16)
        cls.user_1: UserDetail = user
        cls.user_2: UserDetail = user_instance.make()
        cls.url: str = reverse("user:update", kwargs={"user_id": user.user_id})

    def test_accessing_api_without_permission(self):
        """Method to test accessing data without permission or user credential."""
        response: Response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_user_information_invalid_input(self):
        """Method to test editing user information with invalid input."""
        response: Response = self.client.put(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"first_name": secrets.token_hex(16)}
        response: Response = self.client.put(self.url, HTTP_AUTHORIZATION=self.token, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"last_name": secrets.token_hex(16)}
        response: Response = self.client.put(self.url, HTTP_AUTHORIZATION=self.token, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_user_information_valid_input(self):
        """Method to test editing user information with valid input."""
        request_body: Dict[str, str] = {"first_name": self.first_name, "last_name": self.last_name}
        response: Response = self.client.put(self.url, HTTP_AUTHORIZATION=self.token, data=request_body)
        self.user_1.first_name = self.first_name
        self.user_1.last_name = self.last_name
        expected_result: UserDetail = UserEditSerializer(self.user_1).data
        response_data: UserDetail = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_edit_other_user_information(self):
        """Method to test editing other user's information."""
        url: str = reverse("user:update", kwargs={"user_id": self.user_2.user_id})
        request_body: Dict[str, str] = {"first_name": self.first_name, "last_name": self.last_name}
        response: Response = self.client.put(url, HTTP_AUTHORIZATION=self.token, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
