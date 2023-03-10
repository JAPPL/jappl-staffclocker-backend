from django.db import transaction
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.permissions.is_employee_permission import IsEmployeePermission
from jappl_time_log.serializers.user.user_edit_serializer import UserEditSerializer


class UserEditView(UpdateAPIView):
    """API for editing user information."""

    queryset = UserDetail.objects.all()
    lookup_field = "user_id"
    serializer_class = UserEditSerializer
    permission_classes = [IsEmployeePermission]

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs) -> Response:
        """Update user detail that can perform only when edit themselves."""
        if kwargs['user_id'] != request.user.user_id:
            return Response(data={"detail": "Can not edit other users' information."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, args, kwargs)
