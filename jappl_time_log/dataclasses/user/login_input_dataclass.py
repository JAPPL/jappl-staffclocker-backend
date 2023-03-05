from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class LoginInputDataclass:
    """Input dataclass for user login view."""

    email: str
    password: str
