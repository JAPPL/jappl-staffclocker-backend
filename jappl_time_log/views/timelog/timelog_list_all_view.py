from rest_framework.generics import ListAPIView

from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.permissions.is_employee_permission import IsEmployeePermission
from jappl_time_log.serializers.timelog.timelog_read_serializer import TimeLogReadSerializer


class TimeLogListAllView(ListAPIView):
    """API for list all timelog."""

    queryset = TimeLog.objects.all()
    permission_classes = [IsEmployeePermission]
    serializer_class = TimeLogReadSerializer
