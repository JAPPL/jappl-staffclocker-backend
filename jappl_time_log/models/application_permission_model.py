from django.db import models


class ApplicationPermission(models.Model):
    """ApplicationPermission model to keep which users are allowed to access which application."""

    application_permission_id = models.BigAutoField(primary_key=True)
    application_id = models.ForeignKey(to="jappl_time_log.Application", null=False, on_delete=models.PROTECT)
    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", null=False, on_delete=models.CASCADE)

    class Meta:
        """Constraint to have unique user_id and application_id."""

        constraints = [models.UniqueConstraint(fields=["user_id", "application_id"], name="u_user_application")]
