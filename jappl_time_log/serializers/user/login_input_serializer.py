from rest_framework.serializers import CharField, EmailField
from rest_framework_dataclasses.serializers import DataclassSerializer

from jappl_time_log.dataclasses.user.login_input_dataclass import LoginInputDataclass


class LoginInputSerializer(DataclassSerializer):
    """Serializer for user login request data."""

    email = EmailField(help_text="User's email with format")
    password = CharField(help_text="User's password")

    class Meta:
        """Meta data for serializer class.

        See https://pypi.org/project/djangorestframework-dataclasses/ for more detail
        """

        dataclass = LoginInputDataclass
        fields = "__all__"
