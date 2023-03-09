from jappl_time_log.serializers.application.application_permission_write_serializer import (
    ApplicationPermissionWriteSerializer,
)
from jappl_time_log.serializers.application.application_serializer import ApplicationSerializer
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer


class ApplicationPermissionReadSerializer(ApplicationPermissionWriteSerializer):
    """Nested model serializer for application permission."""

    user = UserDetailSerializer()
    application = ApplicationSerializer()
