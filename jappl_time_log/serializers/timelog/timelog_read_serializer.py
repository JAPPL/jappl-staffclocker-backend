from jappl_time_log.serializers.project.project_serializer import ProjectSerializer
from jappl_time_log.serializers.timelog.timelog_input_serializer import TimeLogSerializer
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer


class TimeLogReadSerializer(TimeLogSerializer):
    """Nested model serializer for timelog."""

    user_id = UserDetailSerializer()
    project_id = ProjectSerializer()
