from rest_framework.serializers import ModelSerializer

from jappl_time_log.models.time_log_model import TimeLog


class TimeLogSerializer(ModelSerializer):
    """TimeLog Model serializer."""

    class Meta:
        """Meta data for serializer class.

        See https://pypi.org/project/djangorestframework-dataclasses/ for more detail
        """

        model = TimeLog
        fields = "__all__"
