import json

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestUserListView(APITestCase):
    """Test class for getting user detail."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for listing user test cases."""
        user: UserDetail = user_instance.make(email="test3@gmail.com")
        cls.user: UserDetail = user
        cls.url = reverse("user:detail", kwargs={"user_id": user.user_id})

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.user)

    def test_list_user_with_permission(self):
        """Method to test getting user detail with permission."""
        response: Response = self.client.get(self.url)
        expected_result: UserDetail = UserDetailSerializer(self.user).data
        response_data: UserDetail = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)
