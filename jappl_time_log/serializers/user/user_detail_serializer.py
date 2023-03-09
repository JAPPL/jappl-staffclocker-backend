from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.user_detail_model import UserDetail


class UserDetailSerializer(ModelSerializer):
    """Model serializer for user detail."""

    class Meta:
        """Meta data for serializer class.

        See https://www.django-rest-framework.org/api-guide/serializers/#modelserializer for more detail
        """

        model = UserDetail
        fields = ["user_id", "first_name", "last_name", "email"]
