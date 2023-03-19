from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.serializers.timelog.timelog_read_serializer import TimeLogSerializer


class TimeLogApproveView(UpdateAPIView):
    """API for approving for TimeLog."""

    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs) -> Response:
        """Process UPDATE/PATCH (approving) timelog method for user."""
        try:
            query: TimeLog = TimeLog.objects.get(id=kwargs["pk"])
            this_user: UserDetail = request.user
            timelog_user: UserDetail = query.user_id

            if timelog_user.user_id != this_user.user_id:
                return Response(data={"Can't edit other user."}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response(data={"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        query.approved = True
        query.save()
        serializer = self.get_serializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)