from rest_framework.generics import ListAPIView

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.permissions.is_employee_permission import IsEmployeePermission
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer


class UserListView(ListAPIView):
    """API to list all user."""

    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsEmployeePermission]
