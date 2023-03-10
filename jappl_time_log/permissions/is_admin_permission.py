from typing import Any

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from jappl_time_log.models.role_enum.user_role import UserRole


class IsAdminPermission(BasePermission):
    """Permission to check if user is admin."""

    def has_permission(self, request: Request, view: Any) -> bool:
        """To check if user has admin privilege."""
        return not isinstance(request.user, AnonymousUser) and (request.user.user_role == UserRole.ADMIN)
