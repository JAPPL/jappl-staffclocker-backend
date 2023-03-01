from django.db import models


class UserDetail(models.Model):
    """UserDetail model to keep user data in the database."""

    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
