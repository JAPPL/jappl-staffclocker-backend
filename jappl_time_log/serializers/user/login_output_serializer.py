from rest_framework_dataclasses.serializers import DataclassSerializer

from jappl_time_log.dataclasses.user.login_output_dataclass import LoginOutputDataclass


class LoginOutputSerializer(DataclassSerializer):
    """Serializer for user login response data."""

    class Meta:
        """Meta data for serializer class.

        See https://pypi.org/project/djangorestframework-dataclasses/ for more detail
        """

        dataclass = LoginOutputDataclass
        fields = "__all__"
