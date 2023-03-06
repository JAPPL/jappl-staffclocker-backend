from typing import Any

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class EmployeeOnlyPermission(BasePermission):
    """Permission class to verify user is employee or anonymous user."""

    def has_permission(self, request: Request, view: Any) -> bool:
        """Check permission from request."""
        return not isinstance(request.user, AnonymousUser)
