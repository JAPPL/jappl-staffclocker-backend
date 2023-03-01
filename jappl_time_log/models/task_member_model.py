from django.db import models


class TaskMember(models.Model):
    """TaskMember model to keep user data and tasks to check whether they are PM or not."""

    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", primary_key=True)
    task_id = models.ForeignKey(to="jappl_time_log.Task", primary_key=True)
    is_pm = models.BooleanField(default=False, null=False)
