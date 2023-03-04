from typing import Tuple, Union

from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.dataclasses.user.login_input_dataclass import LoginInputDataclass
from jappl_time_log.models.user_detail_model import UserDetail


class UserAccountService:
    """Service class to handle user detail."""

    @classmethod
    # TODO: Change to check hashed password
    def generate_token(cls, user_data: LoginInputDataclass) -> Tuple[str, Union[UserDetail, None]]:
        """Generate JWT token for user.

        :param user_data: validated data to use to authenticate user
        :return: signed JWT token, user data from database
        """
        user_detail: UserDetail = UserDetail.objects.filter(email__exact=user_data.email).first()
        if (user_detail is not None) and (user_detail.password == user_data.password):
            jwt_token: RefreshToken = RefreshToken.for_user(user=user_detail)
            return jwt_token.access_token, user_detail
        return "", None
