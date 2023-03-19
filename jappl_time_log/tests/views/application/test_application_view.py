import json
import secrets
from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.application_model import Application
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.application.application_serializer import ApplicationSerializer
from jappl_time_log.tests.model_instances.application_model import application_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestApplicationView(APITestCase):
    """Test class for application view sets."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for application test cases."""
        cls.user: UserDetail = user_instance.make(email="test@gmail.com")
        cls.application: Application = application_instance.make()
        cls.new_application_name: str = secrets.token_hex(16)

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.user)

    def test_list_multiple_applications(self):
        """Method to test listing applications."""
        url = reverse("application:list")
        response: Response = self.client.get(url)
        expected_result: List[Application] = [ApplicationSerializer(self.application).data]
        response_data: List[Application] = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_retrieve_application(self):
        """Method to test getting application detail."""
        url = reverse("application:detail", kwargs={"application_id": self.application.application_id})
        response: Response = self.client.get(url)
        expected_result: Application = ApplicationSerializer(self.application).data
        response_data: Application = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_add_application_valid_input(self):
        """Method to test adding application with correct input."""
        url = reverse("application:add")
        request_body: Dict[str, str] = {"application_name": self.new_application_name}
        response: Response = self.client.post(url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_application_invalid_input(self):
        """Method to test adding application with incorrect input."""
        url = reverse("application:add")
        response: Response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_application_valid_input(self):
        """Method to test editing application with correct input."""
        url = reverse("application:update", kwargs={"application_id": self.application.application_id})
        request_body: Dict[str, str] = {"application_name": self.new_application_name}
        response: Response = self.client.put(url, data=request_body)
        self.application.application_name = self.new_application_name
        expected_result: Application = ApplicationSerializer(self.application).data
        response_data: Application = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_edit_application_invalid_input(self):
        """Method to test editing application with incorrect input."""
        url = reverse("application:update", kwargs={"application_id": self.application.application_id})
        response: Response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_application(self):
        """Method to test deleting existing application."""
        url = reverse("application:delete", kwargs={"application_id": self.application.application_id})
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_application_not_found_application(self):
        """Method to test adding non-existing application."""
        url = reverse("application:delete", kwargs={"application_id": self.application.application_id + 1})
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
