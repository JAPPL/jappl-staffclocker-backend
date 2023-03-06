from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.project_model import Project


class ProjectSerializer(ModelSerializer):
    """Project Model serializer."""

    class Meta:
        """Meta data for serializer class.

        See https://pypi.org/project/djangorestframework-dataclasses/ for more detail
        """

        model = Project
        fields = ['project_id', 'project_name']
