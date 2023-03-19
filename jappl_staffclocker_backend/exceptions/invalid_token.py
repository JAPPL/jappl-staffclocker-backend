from rest_framework.exceptions import AuthenticationFailed


class InvalidToken(AuthenticationFailed):
    """Exception for middleware when decode firebase token."""

    pass
