from typing import Dict, Tuple

from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from jappl_time_log.serializers.user.register_input_serializer import RegisterInputSerializer
from jappl_time_log.services.user.user_account_service import UserAccountService


class RegisterView(CreateAPIView):
    """API for user to register account."""

    serializer_class = RegisterInputSerializer

    @transaction.atomic
    def create(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Process request data and register user account.

        :param request: Request from user with format (see swagger for more information)
        :param args: additional arguments
        :param: kwargs: required variable in url
        :return: response with signed token for user identity
        """
        input_serializer: RegisterInputSerializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.validated_data['password'] = UserAccountService.hash_password(
            input_serializer.validated_data['password']
        )
        try:
            input_serializer.save()
        except IntegrityError:
            return Response(data={"detail": "Email already exists."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={"detail": "Register successfully."}, status=status.HTTP_201_CREATED)
