from dataclasses import dataclass

from dataclasses_json import dataclass_json

from jappl_time_log.models.user_detail_model import UserDetail


@dataclass_json
@dataclass
class LoginOutputDataclass:
    """Output dataclass for user login view."""

    first_name: str
    last_name: str
    token: str

    @classmethod
    def from_model(cls, user_instance: UserDetail, token: str) -> "LoginOutputDataclass":
        """Class method to generate dataclass instance with token.

        :param user_instance: user information from database (UserDetail model)
        :param token: generated JWT token
        :return: Instance of this dataclass
        """
        return cls(first_name=user_instance.first_name, last_name=user_instance.last_name, token=token)
