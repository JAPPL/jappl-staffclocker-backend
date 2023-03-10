from django.db import models


class UserRole(models.TextChoices):
    """UserRole enum to keep different user role's."""

    EMPLOYEE = "Employee"
    PM = "Project Manager"
    ADMIN = "Admin"
