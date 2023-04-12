from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.serializers.timelog.timelog_read_serializer import TimeLogReadSerializer


class TimeLogMarkAsPaidView(UpdateAPIView):
    """API for mark time log as paid."""

    serializer_class = TimeLogReadSerializer

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs) -> Response:
        """Process UPDATE/PATCH (mark as paid) timelog method for user."""
        try:
            timelog: TimeLog = TimeLog.objects.get(id=kwargs["pk"])
        except ObjectDoesNotExist as e:
            return Response(data={"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        if not timelog.approved:
            return Response(
                data={"detail": "Time log is not approved yet. Please approve it before mark it as paid."},
                status=status.HTTP_202_ACCEPTED,
            )
        timelog.paid = True
        timelog.save()
        serializer = self.get_serializer(timelog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
