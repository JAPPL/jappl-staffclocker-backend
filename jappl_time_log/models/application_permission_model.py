from django.db import models


class ApplicationPermission(models.Model):
    """ApplicationPermission model to keep which users are allowed to access which application."""

    application_id = models.ForeignKey(to="jappl_time_log.Application", primary_key=True)
    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", primary_key=True)
