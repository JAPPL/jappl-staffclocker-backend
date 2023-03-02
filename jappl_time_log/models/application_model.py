from django.db import models


class Application(models.Model):
    """Application model to keep each application's name(page)."""

    application_id = models.BigAutoField(primary_key=True)
    application_name = models.CharField(max_length=100, null=False)
