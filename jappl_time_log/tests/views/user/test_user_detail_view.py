import json
import secrets

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer
from jappl_time_log.services.user.user_account_service import UserAccountService
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestUserListView(APITestCase):
    """Test class for getting user detail."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for listing user test cases."""
        raw_password: str = secrets.token_hex(16)
        hashed_password: str = UserAccountService.hash_password(raw_password)
        user: UserDetail = user_instance.make(email="test3@gmail.com", password=hashed_password)
        cls.token: str = "Bearer " + str(RefreshToken.for_user(user=user).access_token)
        cls.user: UserDetail = user
        cls.url = reverse("user:detail", kwargs={"user_id": user.user_id})

    def test_list_user_no_permission(self):
        """Method to test accessing user detail API with no permission."""
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user_with_permission(self):
        """Method to test getting user detail with permission."""
        response: Response = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        expected_result: UserDetail = UserDetailSerializer(self.user).data
        response_data: UserDetail = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)
