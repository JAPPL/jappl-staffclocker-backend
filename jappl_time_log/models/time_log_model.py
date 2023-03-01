from django.db import models


class TimeLog(models.Model):
    """TimeLog model to keep log data of each user and each task."""

    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", null=False, on_delete=models.CASCADE)
    hour_spent = models.PositiveIntegerField(null=False)
    message = models.CharField(max_length=100, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    project_id = models.ForeignKey(to="jappl_time_log.Project", null=False, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
