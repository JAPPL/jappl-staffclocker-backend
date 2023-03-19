import json
from typing import List

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestUserListView(APITestCase):
    """Test class for listing user."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for listing user test cases."""
        cls.user_1: UserDetail = user_instance.make()
        cls.user_2: UserDetail = user_instance.make()
        cls.url = reverse("user:list")

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.user_1)

    def test_list_user_with_permission(self):
        """Method to test listing user with permission."""
        response: Response = self.client.get(self.url)
        expected_result: List[UserDetail] = [
            UserDetailSerializer(self.user_1).data,
            UserDetailSerializer(self.user_2).data,
        ]
        response_data: List[UserDetail] = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)
