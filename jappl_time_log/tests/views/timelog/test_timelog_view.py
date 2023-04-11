import json
from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.project_model import Project
from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.timelog.timelog_read_serializer import TimeLogReadSerializer
from jappl_time_log.tests.model_instances.project_instance import project_instance
from jappl_time_log.tests.model_instances.time_log_instance import time_log_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestTimeLogView(APITestCase):
    """Test class for user login."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Mock data for test cases."""
        cls.route: Dict[str:str] = {
            "get": "timelog:timelog_root",
            "create": "timelog:timelog_create",
            "delete": "timelog:timelog_delete",
            "update": "timelog:timelog_update",
        }

        project: Project = project_instance.make(project_name="test_project")
        cls.project = project

        user: UserDetail = user_instance.make(email="test@gmail.com")
        cls.user: UserDetail = user
        cls.timelog: TimeLog = time_log_instance.make(user_id=user, hour_spent=2, message="test", project_id=project)

        user_2: UserDetail = user_instance.make(email="test2@gmail.com")
        cls.user_2: UserDetail = user_2
        cls.timelog_2: TimeLog = time_log_instance.make(
            user_id=user_2, hour_spent=2, message="test", project_id=project
        )

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.user)

    def test_get_timelog(self) -> None:
        """Method to test GET timelog method."""
        url: str = reverse(self.route["get"])
        response: Response = self.client.get(url)
        self.client.force_authenticate(user=self.user_2)
        response_2: Response = self.client.get(url)

        expected_result_1: List[TimeLog] = [
            TimeLogReadSerializer(self.timelog).data,
        ]
        response_data_1: List[TimeLog] = json.loads(json.dumps(response.data))
        expected_result_2: List[TimeLog] = [
            TimeLogReadSerializer(self.timelog_2).data,
        ]
        response_data_2: List[TimeLog] = json.loads(json.dumps(response_2.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_result_1, response_data_1)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_result_2, response_data_2)

    def test_create_timelog(self) -> None:
        """Method to test create timelog."""
        url: str = reverse(self.route["create"])
        data: Dict[str, any] = {
            "hour_spent": 2,
            "message": "test_msg",
            "project_id": self.project.project_id,
            "timestamp": "2022-04-10",
        }
        response: Response = self.client.post(url, data=data)
        self.client.force_authenticate(user=self.user_2)
        response_2: Response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_id"], self.user.user_id)

        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.data["user_id"], self.user_2.user_id)

    def test_create_timelog_no_input(self) -> None:
        """Method to test create timelog with no input."""
        url: str = reverse(self.route["create"])
        response: Response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_timelog(self) -> None:
        """Method to test delete timelog."""
        url: str = reverse(self.route["delete"], args=[self.timelog_2.id])
        self.client.force_authenticate(user=self.user_2)
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_timelog_not_self(self) -> None:
        """Method to test delete timelog that is not self."""
        url: str = reverse(self.route["delete"], args=[self.timelog.id])
        self.client.force_authenticate(user=self.user_2)
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_timelog_not_exist(self) -> None:
        """Method to test delete timelog that doesn't exist."""
        url: str = reverse(self.route["delete"], args=[self.timelog.id + 2])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_timelog(self) -> None:
        """Method to test put timelog."""
        url: str = reverse(self.route["update"], args=[self.timelog.id])
        data: Dict[str, str] = {
            "hour_spent": 4,
            "message": "test2_message",
            "project_id": self.project.project_id,
            "timestamp": "2022-04-08",
        }
        response: Response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["hour_spent"], 4)
        self.assertEqual(response.data["message"], "test2_message")

    def test_put_timelog_not_self(self) -> None:
        """Method to test put timelog that is not self."""
        url: str = reverse(self.route["update"], args=[self.timelog_2.id])
        data: Dict[str, str] = {"hour_spent": 4, "message": "test2_message", "project_id": self.project.project_id}
        response: Response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_timelog_no_input(self) -> None:
        """Method to test put timelog that has no input."""
        url: str = reverse(self.route["update"], args=[self.timelog.id])
        response: Response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_timelog_not_exist(self) -> None:
        """Method to test put timelog that doesn't exist."""
        url: str = reverse(self.route["update"], args=[self.timelog.id + 2])
        data: Dict[str, str] = {"hour_spent": 4, "message": "test2_message", "project_id": self.project.project_id}
        response: Response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_timelog(self) -> None:
        """Method to test patch timelog."""
        url: str = reverse(self.route["update"], args=[self.timelog.id])
        data: Dict[str, str] = {"message": "test3_message"}
        response: Response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "test3_message")

    def test_patch_timelog_not_self(self) -> None:
        """Method to test patch timelog that is not self."""
        url: str = reverse(self.route["update"], args=[self.timelog_2.id])
        data: Dict[str, str] = {"hour_spent": 4, "message": "test2_message", "project_id": self.project.project_id}
        response: Response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_timelog_no_input(self) -> None:
        """Method to test patch timelog that has no input."""
        url: str = reverse(self.route["update"], args=[self.timelog.id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_timelog_not_exist(self) -> None:
        """Method to test patch timelog that doesn't exist."""
        url: str = reverse(self.route["update"], args=[self.timelog.id + 2])
        data: Dict[str, str] = {"message": "test2_message"}
        response: Response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
