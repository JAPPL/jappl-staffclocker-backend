import json
from typing import List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestUserListView(APITestCase):
    """Test class for listing user."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for listing user test cases."""
        user: UserDetail = user_instance.make()
        cls.token: str = "Bearer " + str(RefreshToken.for_user(user=user).access_token)
        cls.user_1: UserDetail = user
        cls.user_2: UserDetail = user_instance.make()
        cls.url = reverse("user:list")

    def test_list_user_no_permission(self):
        """Method to test accessing list user API with no permission."""
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user_with_permission(self):
        """Method to test listing user with permission."""
        response: Response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        expected_result: List[UserDetail] = [
            UserDetailSerializer(self.user_1).data,
            UserDetailSerializer(self.user_2).data,
        ]
        response_data: List[UserDetail] = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)
