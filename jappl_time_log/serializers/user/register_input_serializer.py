from rest_framework.serializers import EmailField, ModelSerializer

from jappl_time_log.models.user_detail_model import UserDetail


class RegisterInputSerializer(ModelSerializer):
    """Serializer for user registration request data."""

    email = EmailField()

    class Meta:
        """Meta data for serializer class.

        See https://www.django-rest-framework.org/api-guide/serializers/#modelserializer for more detail
        """

        model = UserDetail
        fields = ['email', 'password', 'first_name', 'last_name']
