from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request

# from jappl_time_log.models.application_permission_model import ApplicationPermission


class AdminOnly(BasePermission):
    """Permission to check if user is admin."""

    def has_permission(self, request: Request, view: Any) -> bool:
        """To check if user has admin privilege."""
        # Uncomment when permission api is implemented

        # user_id = request.user.user_id
        # permissions = ApplicationPermission.objects.filter(user_id=user_id, application_id=1).values()
        # if permissions < 1:

        # admin_permission = bool(request.user)
        # print(admin_permission)
        return bool(request.user)
