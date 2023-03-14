import json
import secrets
from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.application_model import Application
from jappl_time_log.models.application_permission_model import ApplicationPermission
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.application.application_permission_read_serializer import (
    ApplicationPermissionReadSerializer,
)
from jappl_time_log.serializers.application.application_permission_write_serializer import (
    ApplicationPermissionWriteSerializer,
)
from jappl_time_log.services.user.user_account_service import UserAccountService
from jappl_time_log.tests.model_instances.application_model import application_instance
from jappl_time_log.tests.model_instances.application_permission_instance import application_permission_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestApplicationPermissionView(APITestCase):
    """Test class for application permission view sets."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for application permission test cases."""
        raw_password: str = secrets.token_hex(16)
        hashed_password: str = UserAccountService.hash_password(raw_password)
        application: Application = application_instance.make()
        user: UserDetail = user_instance.make(email="test2@gmail.com", password=hashed_password)
        cls.user_1: UserDetail = user
        cls.user_2: UserDetail = user_instance.make()
        cls.employee_token: str = "Bearer " + str(RefreshToken.for_user(user=user).access_token)
        cls.application_1: Application = application
        cls.application_2: Application = application_instance.make()
        cls.update_url: str = "application:permission-update"
        cls.application_permission: ApplicationPermission = application_permission_instance.make(
            application=application, user=user
        )

    def test_accessing_api_with_invalid_permission(self):
        """Method to test accessing permission api under application with invalid permission."""
        url: str = reverse("application:permission-list")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_multiple_application_permission(self):
        """Method to test listing application permission."""
        url: str = reverse("application:permission-list")
        response: Response = self.client.get(url, HTTP_AUTHORIZATION=self.employee_token)
        expected_result: List[ApplicationPermission] = [
            ApplicationPermissionReadSerializer(self.application_permission).data
        ]
        response_data: List[ApplicationPermission] = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_retrieve_application_permission(self):
        """Method to test getting existing application permission."""
        url: str = reverse(
            "application:permission-detail",
            kwargs={"application_permission_id": self.application_permission.application_permission_id},
        )
        response: Response = self.client.get(url, HTTP_AUTHORIZATION=self.employee_token)
        expected_result: Application = ApplicationPermissionReadSerializer(self.application_permission).data
        response_data: Application = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_retrieve_application_permission_not_found(self):
        """Method to test getting non-existing application permission."""
        url: str = reverse(
            "application:permission-detail",
            kwargs={"application_permission_id": self.application_permission.application_permission_id + 1},
        )
        response: Response = self.client.get(url, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_application_permission_valid_input(self):
        """Method to test adding application with correct input."""
        url: str = reverse("application:permission-add")
        request_body: Dict[str, str] = {"application": self.application_1.application_id, "user": self.user_2.user_id}
        response: Response = self.client.post(url, data=request_body, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_application_permission_invalid_input(self):
        """Method to test adding application permission with incorrect input."""
        url: str = reverse("application:permission-add")
        response: Response = self.client.post(url, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_application_permission_valid_input(self):
        """Method to test editing application permission with correct input."""
        url: str = reverse(
            self.update_url, kwargs={"application_permission_id": self.application_permission.application_permission_id}
        )
        request_body: Dict[str, str] = {"application": self.application_2.application_id, "user": self.user_1.user_id}
        response: Response = self.client.put(url, data=request_body, HTTP_AUTHORIZATION=self.employee_token)
        self.application_permission.application = self.application_2
        expected_result: Application = ApplicationPermissionWriteSerializer(self.application_permission).data
        response_data: Application = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_edit_application_permission_invalid_input(self):
        """Method to test editing application permission with incorrect input."""
        url: str = reverse(
            self.update_url, kwargs={"application_permission_id": self.application_permission.application_permission_id}
        )
        response: Response = self.client.put(url, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_application_permission_not_found(self):
        """Method to test editing non-existing application permission."""
        url: str = reverse(
            self.update_url,
            kwargs={"application_permission_id": self.application_permission.application_permission_id + 1},
        )
        response: Response = self.client.put(url, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_application_permission(self):
        """Method to test deleting existing application permission."""
        url = reverse(
            "application:permission-delete",
            kwargs={"application_permission_id": self.application_permission.application_permission_id},
        )
        response: Response = self.client.delete(url, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_application_permission_not_found(self):
        """Method to test deleting non-existing application permission."""
        url = reverse(
            "application:permission-delete",
            kwargs={"application_permission_id": self.application_permission.application_permission_id + 1},
        )
        response: Response = self.client.delete(url, HTTP_AUTHORIZATION=self.employee_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
