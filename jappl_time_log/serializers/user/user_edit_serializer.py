from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.user_detail_model import UserDetail


class UserEditSerializer(ModelSerializer):
    """Model serializer for user edit request."""

    class Meta:
        """Meta data for serializer class.

        See https://www.django-rest-framework.org/api-guide/serializers/#modelserializer for more detail
        """

        model = UserDetail
        fields = ["user_id", "first_name", "last_name"]
