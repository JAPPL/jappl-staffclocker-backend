from typing import Union

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from jappl_time_log.models.application_permission_model import ApplicationPermission
from jappl_time_log.permissions.is_admin_permission import IsAdminPermission
from jappl_time_log.serializers.application.application_permission_read_serializer import (
    ApplicationPermissionReadSerializer,
)
from jappl_time_log.serializers.application.application_permission_write_serializer import (
    ApplicationPermissionWriteSerializer,
)


class ApplicationPermissionViewSet(ModelViewSet):
    """API view set for application permission."""

    queryset = ApplicationPermission.objects.all()
    serializer_classes = {
        "retrieve": ApplicationPermissionReadSerializer,
        "create": ApplicationPermissionWriteSerializer,
        "update": ApplicationPermissionWriteSerializer,
        "list": ApplicationPermissionReadSerializer,
    }
    permission_classes = [IsAdminPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['application', 'user']
    search_fields = ['application__application_name', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['application', 'user']
    lookup_field = "application_permission_id"

    def get_serializer_class(
        self,
    ) -> Union[ApplicationPermissionWriteSerializer, ApplicationPermissionReadSerializer, None]:
        """Get serializer class according to request method."""
        return self.serializer_classes.get(self.action)
