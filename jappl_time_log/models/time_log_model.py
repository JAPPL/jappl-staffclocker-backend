from django.db import models


class TimeLog(models.Model):
    """TimeLog model to keep log data of each user and each task."""

    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", null=False)
    hour_spent = models.PositiveIntegerField(null=False)
    message = models.CharField(max_length=100, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    task_id = models.ForeignKey(to="jappl_time_log.Task", null=False)
    approved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
