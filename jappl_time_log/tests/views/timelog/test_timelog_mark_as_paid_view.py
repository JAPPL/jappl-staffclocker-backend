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


class TestTimeLogMarkAsPaidView(APITestCase):
    """Test class for marking timelog as paid."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for timelog list test cases."""
        user_1: UserDetail = user_instance.make()
        project_1: Project = project_instance.make(project_name="test_project")
        cls.user_1: UserDetail = user_1
        cls.project_1 = project_1
        cls.approved_timelog_1: TimeLog = time_log_instance.make(
            user_id=user_1, hour_spent=2, message="test approved timelog", project_id=project_1, approved=True
        )
        cls.timelog_1: TimeLog = time_log_instance.make(
            user_id=user_1, hour_spent=2, message="test not approved timelog", project_id=project_1, approved=False
        )

        user_2: UserDetail = user_instance.make()
        cls.user_2: UserDetail = user_2
        cls.timelog_2: TimeLog = time_log_instance.make(
            user_id=user_2, hour_spent=2, message="test", project_id=project_1
        )
        cls.url: str = "timelog:timelog_mark_as_paid"

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.user_1)

    def test_mark_as_paid_approved_timelog_with_permission(self):
        """Method to test marking approved timelog as paid."""
        url: str = reverse(self.url, args=[self.approved_timelog_1.id])
        response: Response = self.client.patch(url)
        response_data: TimeLog = json.loads(json.dumps(response.data))
        self.assertEqual(True, response_data['paid'])

    def test_mark_as_paid_not_approved_timelog_with_permission(self):
        """Method to test marking not approved timelog as paid."""
        url: str = reverse(self.url, args=[self.timelog_1.id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_mark_timelog_with_no_permission(self) -> None:
        """Method to test marking other users' timelog."""
        url: str = reverse(self.url, args=[self.timelog_2.id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_timelog_no_input(self) -> None:
        """Method to test marking approved timelog as paid without input."""
        url: str = reverse(self.url, args=[self.approved_timelog_1.id])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_non_existing_timelog(self) -> None:
        """Method to test marking timelog that doesn't exist."""
        url: str = reverse(self.url, args=[self.timelog_1.id + 6])
        response: Response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
