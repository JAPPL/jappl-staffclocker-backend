from django.db import models


class ProjectMember(models.Model):
    """ProjectMember model to keep user data and projects to check whether they are PM or not."""

    project_member_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(to="jappl_time_log.UserDetail", null=False, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to="jappl_time_log.Project", null=False, on_delete=models.CASCADE)
    is_pm = models.BooleanField(default=False, null=False)

    class Meta:
        """Constraint to have unique user_id and project_id."""

        constraints = [models.UniqueConstraint(fields=["user_id", "project_id"], name="u_user_project")]
