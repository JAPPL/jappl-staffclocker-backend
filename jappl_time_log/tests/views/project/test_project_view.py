from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from jappl_time_log.tests.model_instances.project_instance import project_instance


class TestRegisterView(APITestCase):
    """Test class for user login."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Mock data for test cases."""
        project_names: List[str] = ["Test_Project_1", "Test_Project_2", "Test_Project_3"]
        for name in project_names:
            project_instance.make(project_name=name)
        cls.project_names: str = project_names

    def test_get_project(self) -> None:
        """Method to test project call."""
        url: str = reverse("project:project_root")
        response: Response = self.client.get(url)
        name_list = list(map(lambda e: e["projectName"], response.json()))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(name_list, self.project_names)

    def test_create_project(self) -> None:
        """Method to test create project."""
        url: str = reverse("project:project_create")
        project_name: str = "Test_Project_2"
        request_body: Dict[str, str] = {"project_name": project_name}
        response: Response = self.client.post(url, data=request_body)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["project_name"], project_name)
        self.assertIsNotNone(response.data["project_id"])

    def test_create_project_invalid_input(self) -> None:
        """Method to test create project with invalid input."""
        url: str = reverse("project:project_create")
        response: Response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_update_project(self) -> None:
        """Method to test update exisiting project."""
        url: str = reverse("project:project_update", args=[1])
        project_name: str = "Test_Project_New"
        request_body: Dict[str, str] = {"project_name": project_name}
        response: Response = self.client.patch(url, data=request_body)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], project_name)
        self.assertIsNotNone(response.data['project_id'])

    def test_put_update_project(self) -> None:
        """Method to test update exisiting project."""
        url: str = reverse("project:project_update", args=[2])
        project_name: str = "Test_Project"
        request_body: Dict[str, str] = {"project_name": project_name}
        response: Response = self.client.put(url, data=request_body)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], project_name)
        self.assertIsNotNone(response.data['project_id'])

    def test_patch_update_project_empty_input(self) -> None:
        """Method to test update (PATCH) existing project with empty input."""
        url: str = reverse("project:project_update", args=[1])
        response: Response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_update_project_invalid_input(self) -> None:
        """Method to test update (PUT) existing project with invalid input."""
        url: str = reverse("project:project_update", args=[1])
        response: Response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self) -> None:
        """Method to test delete project."""
        url: str = reverse("project:project_delete", args=[3])
        response: Response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_not_exist(self) -> None:
        """Method to test delete project that doesn't exist."""
        url: str = reverse("project:project_delete", args=[69])
        response: Response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
