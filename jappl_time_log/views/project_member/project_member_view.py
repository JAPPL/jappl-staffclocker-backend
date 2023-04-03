from typing import Union

from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from jappl_time_log.models.project_member_model import ProjectMember
from jappl_time_log.serializers.project_member.project_member_read_serializer import ProjectMemberReadSerializer
from jappl_time_log.serializers.project_member.project_member_serializer import ProjectMemberSerializer


class ProjectMemberViewSet(ModelViewSet):
    """API view set for project member master data."""

    queryset = ProjectMember.objects.all()
    serializer_classes = {
        "retrieve": ProjectMemberReadSerializer,
        "create": ProjectMemberSerializer,
        "update": ProjectMemberSerializer,
        "partial_update": ProjectMemberSerializer,
        "list": ProjectMemberReadSerializer,
    }
    lookup_field = "project_member_id"
    duplication_response_body = "User already in this project."

    def get_serializer_class(
        self,
    ) -> Union[ProjectMemberReadSerializer, ProjectMemberSerializer, None]:
        """Get serializer class according to request method."""
        return self.serializer_classes.get(self.action)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Process POST request for adding project member."""
        try:
            return super().create(request, args, kwargs)
        except IntegrityError:
            return Response(data={"detail": self.duplication_response_body}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs) -> Response:
        """Process PATCH request for adding project member."""
        try:
            return super().update(request, args, kwargs)
        except IntegrityError:
            return Response(data={"detail": self.duplication_response_body}, status=status.HTTP_400_BAD_REQUEST)
