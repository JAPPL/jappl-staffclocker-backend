import json
from typing import List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.timelog.timelog_read_serializer import TimeLogReadSerializer
from jappl_time_log.tests.model_instances.time_log_instance import time_log_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestTimeLogListAllView(APITestCase):
    """Test class for listing all timelog."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for timelog list test cases."""
        user: UserDetail = user_instance.make(email="test@gmail.com")
        cls.token: str = "Bearer " + str(RefreshToken.for_user(user=user).access_token)
        cls.timelog_1: TimeLog = time_log_instance.make()
        cls.timelog_2: TimeLog = time_log_instance.make()
        cls.url: str = reverse("timelog:timelog_list_all")

    def test_list_all_timelog_without_permission(self):
        """Method to test accessing API with no permission."""
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list__all_timelog_with_permission(self):
        """Method to test listing all timelog."""
        response: Response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        expected_result: List[TimeLog] = [
            TimeLogReadSerializer(self.timelog_1).data,
            TimeLogReadSerializer(self.timelog_2).data,
        ]
        response_data: List[TimeLog] = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)
