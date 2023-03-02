from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from jappl_time_log.models.user_detail_model import UserDetail


class JWTTokenAuthentication(JWTAuthentication):
    """Custom middleware for authenticate using jwt.

    Change look up model to default auth user to user detail model in another application
    """

    def get_user(self, validated_token: AccessToken) -> UserDetail:
        """Find and return a user using the given validated token."""
        try:
            user_id: int = validated_token[api_settings.USER_ID_CLAIM]
            user: UserDetail = UserDetail.objects.get(user_id=user_id)
        except KeyError:
            raise InvalidToken(detail="Token contained no recognizable user identification")
        except UserDetail.DoesNotExist:
            raise InvalidToken(detail="User not found", code="user_not_found")

        return user
