from django.core.validators import MaxValueValidator
from django.db import models


class TimeLog(models.Model):
    """TimeLog model to keep log data of each user and each task."""

    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", null=False, on_delete=models.CASCADE)
    hour_spent = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(8)])
    message = models.CharField(max_length=100, null=False)
    timestamp = models.DateTimeField()
    project_id = models.ForeignKey(to="jappl_time_log.Project", null=False, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
