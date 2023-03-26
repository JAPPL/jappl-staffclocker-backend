from typing import Dict, Tuple, Union

import jwt
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from jappl_staffclocker_backend.exceptions.invalid_token import InvalidToken
from jappl_staffclocker_backend.serializer.firebase_payload_serializer import (
    FirebasePayLoadDataclass,
    FirebasePayloadSerializer,
)
from jappl_time_log.models.user_detail_model import UserDetail


class JWTTokenSchema(OpenApiAuthenticationExtension):
    """OpenAPI schema for custom JWT token authentication middleware."""

    target_class = "jappl_staffclocker_backend.middlewares.jwt_authentication_middleware.JWTTokenAuthentication"
    name = "BearerAuthentication"

    def get_security_definition(self, _auto_schema) -> Dict[str, str]:
        """Get security definition for swagger."""
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "Bearer",
        }


def get_first_and_last_name(name: str) -> Tuple[str, str]:
    """Get first name and last name from firebase token payload."""
    first_name, last_name = name.split(" ", 1)
    return first_name, last_name


class JWTTokenAuthentication(BaseAuthentication):
    """Custom middleware for authenticate using jwt.

    Change look up model to default auth user to user detail model in another application
    """

    def authenticate(self, request: Request) -> Union[Tuple[Union[UserDetail, None], None], None]:
        """Authenticate firebase token and insert new user if does not exist."""
        authentication_header: str = request.headers.get("Authorization")
        if not authentication_header:
            return None
        try:
            _, firebase_token = authentication_header.split(' ', 1)
            if not firebase_token:
                return None
            decoded_token: Dict[str, str] = jwt.decode(firebase_token, options={"verify_signature": False})
        except jwt.DecodeError:
            raise InvalidToken("Invalid auth token")
        except ValueError:
            raise InvalidToken("No token given or token is in wrong format")
        token_payload: FirebasePayLoadDataclass = FirebasePayloadSerializer(decoded_token).data
        first_name, last_name = get_first_and_last_name(token_payload.get('name'))
        try:
            user: UserDetail = UserDetail.objects.get(email__exact=token_payload.get("email"))
        except UserDetail.DoesNotExist:
            user: UserDetail = UserDetail.objects.create(
                email=token_payload.get("email"), first_name=first_name, last_name=last_name
            )
        return user, None
