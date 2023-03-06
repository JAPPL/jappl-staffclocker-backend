from rest_framework.viewsets import ModelViewSet

from jappl_time_log.models.application_model import Application
from jappl_time_log.permissions.employee_only_permission import EmployeeOnlyPermission
from jappl_time_log.serializers.application.application_serializer import ApplicationSerializer


class ApplicationViewSet(ModelViewSet):
    """API view set for application master data."""

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [EmployeeOnlyPermission]
    lookup_field = "application_id"
