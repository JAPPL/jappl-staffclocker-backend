from typing import Dict, Tuple

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from jappl_time_log.dataclasses.user.login_input_dataclass import LoginInputDataclass
from jappl_time_log.dataclasses.user.login_output_dataclass import LoginOutputDataclass
from jappl_time_log.serializers.user.login_input_serializer import LoginInputSerializer
from jappl_time_log.serializers.user.login_output_serializer import LoginOutputSerializer
from jappl_time_log.services.user.user_account_service import UserAccountService


class LoginView(GenericAPIView):
    """API for user to login."""

    serializer_class = LoginInputSerializer

    def post(self, request: Request, *args: Tuple[str, str], **kwargs: Dict[str, int]) -> Response:
        """Process request data and validate user account .

        :param request: Request from user with format (see swagger for more information)
        :param args: additional arguments
        :param: kwargs: required variable in url
        :return: response with signed token for user identity
        """
        input_serializer: LoginInputSerializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data: LoginInputDataclass = input_serializer.validated_data
        token, user_detail = UserAccountService.generate_token(user_data=validated_data)
        if user_detail is None:
            return Response(data={"detail": "invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        output_data: LoginOutputDataclass = LoginOutputDataclass.from_model(user_instance=user_detail, token=token)
        response_data: LoginOutputSerializer = LoginOutputSerializer(output_data)
        return Response(data=response_data.data, status=status.HTTP_200_OK)
