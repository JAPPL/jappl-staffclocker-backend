from django.db import models

from jappl_time_log.models.role_enum.user_role import UserRole


class UserDetail(models.Model):
    """UserDetail model to keep user data in the database."""

    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False, blank=False, help_text="User's first name")
    last_name = models.CharField(max_length=100, null=False, blank=False, help_text="User's last name")
    email = models.CharField(max_length=100, null=False, blank=False, unique=True, help_text="User's email")
    password = models.CharField(max_length=100, null=False, blank=False, help_text="User's hashed password")
    user_role = models.CharField(
        max_length=100, null=False, blank=False, choices=UserRole.choices, help_text="User's role"
    )
