import json
import secrets

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.project_model import Project
from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.services.user.user_account_service import UserAccountService
from jappl_time_log.tests.model_instances.project_instance import project_instance
from jappl_time_log.tests.model_instances.time_log_instance import time_log_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestTimeLogApproveView(APITestCase):
    """Test class for listing all timelog."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for timelog list test cases."""
        raw_password: str = secrets.token_hex(16)
        hashed_password: str = UserAccountService.hash_password(raw_password)
        user: UserDetail = user_instance.make(email="test@gmail.com", password=hashed_password)
        cls.user: UserDetail = user
        cls.token: str = "Bearer " + str(RefreshToken.for_user(user=user).access_token)
        project: Project = project_instance.make(project_name="test_project")
        cls.project = project
        cls.timelog_1: TimeLog = time_log_instance.make(user_id=user, hour_spent=2, message="test", project_id=project)

        user_2: UserDetail = user_instance.make(email="test2@gmail.com", password=hashed_password)
        cls.user_2: UserDetail = user_2
        cls.token_2: str = "Bearer " + str(RefreshToken.for_user(user=user_2).access_token)
        cls.timelog_2: TimeLog = time_log_instance.make(
            user_id=user_2, hour_spent=2, message="test", project_id=project
        )
        cls.url: str = "timelog:timelog_approve"

    def test_approve_timelog_with_permission(self):
        """Method to test approving timelog."""
        url: str = reverse(self.url, args=[self.timelog_1.id])
        response: Response = self.client.patch(url, HTTP_AUTHORIZATION=self.token)
        response_data: TimeLog = json.loads(json.dumps(response.data))
        self.assertEqual(True, response_data['approved'])

    def test_approve_timelog_with_no_permission(self) -> None:
        """Method to test approving timelog of different user ."""
        url: str = reverse(self.url, args=[self.timelog_2.id])
        response: Response = self.client.patch(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_approve_timelog_no_input(self) -> None:
        """Method to test approving timelog that has no input."""
        url: str = reverse(self.url, args=[self.timelog_1.id])
        response: Response = self.client.patch(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_approve_timelog_not_exist(self) -> None:
        """Method to test approving timelog that doesn't exist."""
        url: str = reverse(self.url, args=[self.timelog_1.id + 6])
        response: Response = self.client.patch(url, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
