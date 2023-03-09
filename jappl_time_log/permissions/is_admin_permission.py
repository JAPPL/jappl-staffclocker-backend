from typing import Any

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAdminPermission(BasePermission):
    """Permission to check if user is admin."""

    def has_permission(self, request: Request, view: Any) -> bool:
        """To check if user has admin privilege."""
        return not isinstance(request.user, AnonymousUser) and request.user.is_super_admin
