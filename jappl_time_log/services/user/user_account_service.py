from typing import Tuple, Union

import argon2
from argon2.exceptions import InvalidHash, VerifyMismatchError
from rest_framework_simplejwt.tokens import RefreshToken

from jappl_time_log.dataclasses.user.login_input_dataclass import LoginInputDataclass
from jappl_time_log.models.user_detail_model import UserDetail


class UserAccountService:
    """Service class to handle user detail."""

    @classmethod
    def generate_token(cls, user_data: LoginInputDataclass) -> Tuple[str, Union[UserDetail, None]]:
        """Generate JWT token for user.

        :param user_data: validated data to use to authenticate user
        :return: signed JWT token, user data from database
        """
        user_detail: UserDetail = UserDetail.objects.filter(email__exact=user_data.email).first()
        if user_detail is not None:
            argon2_hasher = argon2.PasswordHasher()
            hashed_password = user_detail.password
            try:
                argon2_hasher.verify(hashed_password, user_data.password)
                jwt_token: RefreshToken = RefreshToken.for_user(user=user_detail)
                return jwt_token.access_token, user_detail
            except InvalidHash:
                print(f"User {user_detail.user_id} has invalid hashed password in database.")
            except VerifyMismatchError:
                pass
        return "", None

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash raw password for inserting to database.

        :param password: raw password
        :return: hashed password by Argon2
        """
        argon2_hasher = argon2.PasswordHasher()
        hashed_password = argon2_hasher.hash(password=password)
        return hashed_password
