from django.db import models


class UserDetail(models.Model):
    """UserDetail model to keep user data in the database."""

    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False, blank=False, help_text="User's first name")
    last_name = models.CharField(max_length=100, null=False, blank=False, help_text="User's last name")
    email = models.CharField(max_length=100, null=False, blank=False, unique=True, help_text="User's email")
    password = models.CharField(max_length=100, null=False, blank=False, help_text="User's hashed password")
