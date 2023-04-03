import json
from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.models.project_member_model import ProjectMember
from jappl_time_log.models.project_model import Project
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.project_member.project_member_read_serializer import ProjectMemberReadSerializer
from jappl_time_log.serializers.project_member.project_member_serializer import ProjectMemberSerializer
from jappl_time_log.tests.model_instances.project_instance import project_instance
from jappl_time_log.tests.model_instances.project_member_instance import project_member_instance
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestProjectMemberView(APITestCase):
    """Test class for project member view sets."""

    @classmethod
    def setUpTestData(cls):
        """Mock data for project member test cases."""
        employee_1: UserDetail = user_instance.make()
        project_1: Project = project_instance.make()
        project_2: Project = project_instance.make()
        cls.update_url: str = "project_member:update"
        cls.project_1: Project = project_1
        cls.project_2: Project = project_2
        cls.employee_1: UserDetail = employee_1
        cls.employee_2: UserDetail = user_instance.make()
        cls.project_member: ProjectMember = project_member_instance.make(project=project_1, user=employee_1)
        cls.project_member_2: ProjectMember = project_member_instance.make()
        cls.project_member_3: ProjectMember = project_member_instance.make()

    def setUp(self) -> None:
        """Authenticate user for passing through API permission guard."""
        self.client.force_authenticate(user=self.employee_1)

    def test_list_project_member(self):
        """Method to test listing project members."""
        url: str = reverse("project_member:list")
        response: Response = self.client.get(url)
        expected_result: List[ProjectMember] = [
            ProjectMemberReadSerializer(self.project_member).data,
            ProjectMemberReadSerializer(self.project_member_2).data,
            ProjectMemberReadSerializer(self.project_member_3).data,
        ]
        response_data: List[ProjectMember] = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_retrieve_project_member(self):
        """Method to test getting one project's project members."""
        url: str = reverse(
            "project_member:detail",
            kwargs={"project_member_id": self.project_member.project_member_id},
        )
        response: Response = self.client.get(url)
        expected_result: ProjectMember = ProjectMemberReadSerializer(self.project_member).data
        response_data: ProjectMember = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_retrieve_project_member_not_found(self):
        """Method to test getting non-existing project mebmers."""
        url: str = reverse(
            "project_member:detail",
            kwargs={"project_member_id": self.project_member.project_member_id + 10},
        )
        response: Response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_project_member_valid_input(self):
        """Method to test adding project_member with correct input."""
        url: str = reverse("project_member:add")
        request_body: Dict[str, str] = {"project": self.project_2.project_id, "user": self.employee_2.user_id}
        response: Response = self.client.post(url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_project_member_invalid_input(self):
        """Method to test adding project_member with incorrect input, including duplicate."""
        url: str = reverse("project_member:add")
        response: Response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {"project": self.project_1.project_id, "user": self.employee_1.user_id}
        response: Response = self.client.post(url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_project_member_valid_input(self):
        """Method to test editing project_member with correct input."""
        url: str = reverse(self.update_url, kwargs={"project_member_id": self.project_member.project_member_id})
        request_body: Dict[str, str] = {"project": self.project_2.project_id, "user": self.employee_1.user_id}
        response: Response = self.client.put(url, data=request_body)
        self.project_member.project = self.project_2
        expected_result: Project = ProjectMemberSerializer(self.project_member).data
        response_data: Project = json.loads(json.dumps(response.data))
        self.assertEqual(expected_result, response_data)

    def test_edit_project_member_invalid_input(self):
        """Method to test editing project member with incorrect input."""
        url: str = reverse(self.update_url, kwargs={"project_member_id": self.project_member.project_member_id})
        response: Response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body: Dict[str, str] = {
            "project": self.project_member_2.project.project_id,
            "user": self.project_member_2.user.user_id,
        }
        response: Response = self.client.put(url, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_project_member_not_found(self):
        """Method to test editing non-existing project member."""
        url: str = reverse(self.update_url, kwargs={"project_member_id": self.project_member_3.project_member_id + 1})
        response: Response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_project_member(self):
        """Method to test deleting existing project member."""
        url = reverse(
            "project_member:delete",
            kwargs={"project_member_id": self.project_member.project_member_id},
        )
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_member_not_found(self):
        """Method to test deleting non-existing project member."""
        url = reverse(
            "project_member:delete",
            kwargs={"project_member_id": self.project_member_3.project_member_id + 1},
        )
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
