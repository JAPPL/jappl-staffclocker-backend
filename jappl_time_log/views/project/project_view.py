from rest_framework.viewsets import ModelViewSet

from jappl_time_log.models.project_model import Project
from jappl_time_log.serializers.project.project_serializer import ProjectSerializer


class ProjectView(ModelViewSet):
    """API for CRUD Ops for Project."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsEmployeePermission]
