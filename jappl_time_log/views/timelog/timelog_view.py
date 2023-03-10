from typing import Dict, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import QueryDict
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from jappl_time_log.models.time_log_model import TimeLog
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.permissions.is_employee_permission import IsEmployeePermission
from jappl_time_log.serializers.timelog.timelog_input_serializer import TimeLogSerializer


class TimeLogView(ModelViewSet):
    """API for CRUD Ops for Project."""

    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer
    permission_classes = [IsEmployeePermission]

    @transaction.atomic
    def list(self, request: Request) -> Response:
        """Process GET timelog method for user."""
        user: UserDetail = request.user
        queryset = TimeLog.objects.filter(user_id=user.user_id)
        serializer = TimeLogSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Process request data and add timelog for user.

        :param request: Request from user with format (see swagger for more information)
        :param args: additional arguments
        :param: kwargs: required variable in url
        :return: response with signed token for user identity
        """
        user: UserDetail = request.user
        data_with_user_id: QueryDict = QueryDict(f"user_id={user.user_id}", mutable=True)
        data_with_user_id.update(request.data.copy())
        input_serializer: TimeLogSerializer = self.serializer_class(data=data_with_user_id)
        input_serializer.is_valid(raise_exception=True)

        input_serializer.save()
        return Response(data=input_serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Process DELETE timelog method for user."""
        try:
            query: TimeLog = TimeLog.objects.get(id=kwargs["pk"])
            this_user: UserDetail = request.user
            timelog_user: UserDetail = query.user_id

            if timelog_user.user_id != this_user.user_id:
                return Response(data={"Can't edit other user."}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response(data={"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def update(self, request: Request, *args, **kwargs) -> Response:
        """Process UPDATE/PATCH timelog method for user."""
        try:
            query: TimeLog = TimeLog.objects.get(id=kwargs["pk"])
            this_user: UserDetail = request.user
            timelog_user: UserDetail = query.user_id

            if timelog_user.user_id != this_user.user_id:
                return Response(data={"Can't edit other user."}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            return Response(data={"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        user: UserDetail = request.user
        data_with_user_id: QueryDict = QueryDict(f"user_id={user.user_id}", mutable=True)
        data_with_user_id.update(request.data.copy())

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data_with_user_id, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
