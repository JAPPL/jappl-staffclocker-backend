from typing import List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.tests.model_instances.project_instance import project_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestProjectMemberView(APITestCase):
    """Test class for project member view sets."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for project member test cases."""
        employee: UserDetail = user_instance.make()
        cls.employee_token: str = "Bearer " + str(RefreshToken.for_user(user=employee).access_token)
        project_names: List[str] = ["Test_Project_1", "Test_Project_2", "Test_Project_3"]
        for name in project_names:
            project_instance.make(project_name=name)
        cls.project_names: List[str] = project_names
        cls.update_url: str = "project:project_update"

    def test_accessing_api_with_invalid_permission(self):
        """Method to test accessing project member api with invalid permission."""
        url: str = reverse("project_member:list")
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response: Response = self.client.get(url, HTTP_AUTHORIZATION=self.admin_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_list_project_member(self):
    #     """Method to test listing project members."""
    #     url: str = reverse("project_member:list")
    #     response: Response = self.client.get(url, HTTP_AUTHORIZATION=self.super_admin_token)
    #     expected_result: List[ProjectMember] = [
    #         ProjectMemberSerializer(self.project_member).data
    #     ]
    #     response_data: List[ProjectMember] = json.loads(json.dumps(response.data))
    #     self.assertEqual(expected_result, response_data)
