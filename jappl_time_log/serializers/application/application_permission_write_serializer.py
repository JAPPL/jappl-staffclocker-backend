from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.application_permission_model import ApplicationPermission


class ApplicationPermissionWriteSerializer(ModelSerializer):
    """One dimensional model serializer for application permission."""

    class Meta:
        """Meta data for serializer class.

        See https://www.django-rest-framework.org/api-guide/serializers/#modelserializer for more detail
        """

        model = ApplicationPermission
        fields = "__all__"
