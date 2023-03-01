from django.db import models


class Task(models.Model):
    """Task model to keep tasks and task's name."""

    task_id = models.BigAutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
