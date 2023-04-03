from django.db import models


class Project(models.Model):
    """Project model to keep projects and project's name."""

    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=100, unique=True, null=False)
