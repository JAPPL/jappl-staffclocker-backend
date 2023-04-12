import json

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.project_model import Project
from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.tests.model_instances.project_instance import project_instance
from jappl_time_log.tests.model_instances.time_log_instance import time_log_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestTimeLogApproveView(APITestCase):
    """Test class for listing all timelog."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for timelog list test cases."""
        user: UserDetail = user_instance.make()
        cls.user: UserDetail = user
        project: Project = project_instance.make(project_name="test_project")
        cls.project = project
        cls.timelog_1: TimeLog = time_log_instance.make(user_id=user, hour_spent=2, message="test", project_id=project)

        user_2: UserDetail = user_instance.make()
        cls.user_2: UserDetail = user_2
        cls.timelog_2: TimeLog = time_log_instance.make(
            user_id=user_2, hour_spent=2, message="test", project_id=project
        )
        cls.url: str = "timelog:timelog_approve"

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.user)

    def test_approve_timelog(self):
        """Method to test approving timelog."""
        url: str = reverse(self.url, args=[self.timelog_1.id])
        response: Response = self.client.patch(url)
        response_data: TimeLog = json.loads(json.dumps(response.data))
        self.assertEqual(True, response_data['approved'])

    def test_approve_timelog_other_users(self) -> None:
        """Method to test approving timelog of different user ."""
        url: str = reverse(self.url, args=[self.timelog_2.id])
        response: Response = self.client.patch(url)
        response_data: TimeLog = json.loads(json.dumps(response.data))
        self.assertEqual(True, response_data['approved'])

    def test_approve_timelog_no_input(self) -> None:
        """Method to test approving timelog that has no input."""
        url: str = reverse(self.url, args=[self.timelog_1.id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_approve_timelog_not_exist(self) -> None:
        """Method to test approving timelog that doesn't exist."""
        url: str = reverse(self.url, args=[self.timelog_1.id + 6])
        response: Response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
