from rest_framework.generics import RetrieveAPIView

from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.user.user_detail_serializer import UserDetailSerializer


class UserDetailView(RetrieveAPIView):
    """API for getting user detail."""

    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "user_id"
