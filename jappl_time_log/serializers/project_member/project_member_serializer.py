from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.project_member_model import ProjectMember


class ProjectMemberSerializer(ModelSerializer):
    """Model serializer for project member."""

    class Meta:
        """Meta data for serializer class.

        See https://www.django-rest-framework.org/api-guide/serializers/#modelserializer for more detail
        """

        model = ProjectMember
        fields = "__all__"
