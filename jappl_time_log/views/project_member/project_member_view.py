from rest_framework.viewsets import ModelViewSet

from jappl_time_log.models.project_member_model import ProjectMember
from jappl_time_log.permissions.is_admin_permission import IsAdminPermission
from jappl_time_log.permissions.is_pm_permission import IsPmPermission
from jappl_time_log.serializers.project_member.project_member_serializer import ProjectMemberSerializer


class ProjectMemberViewSet(ModelViewSet):
    """API view set for project member master data."""

    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAdminPermission, IsPmPermission]
    lookup_field = "project_member_id"
