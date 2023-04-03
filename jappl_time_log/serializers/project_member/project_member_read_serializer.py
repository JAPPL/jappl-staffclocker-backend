from jappl_time_log.serializers.project.project_serializer import ProjectSerializer
from jappl_time_log.serializers.project_member.project_member_serializer import ProjectMemberSerializer
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer


class ProjectMemberReadSerializer(ProjectMemberSerializer):
    """Nested model serializer for project member detail."""

    user = UserDetailSerializer()
    project = ProjectSerializer()
