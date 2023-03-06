from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.application_model import Application


class ApplicationSerializer(ModelSerializer):
    """Model serializer for application."""

    class Meta:
        """Meta data for serializer class.

        See https://www.django-rest-framework.org/api-guide/serializers/#modelserializer for more detail
        """

        model = Application
        fields = "__all__"
