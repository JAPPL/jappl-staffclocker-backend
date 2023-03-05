from django.test import TestCase
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from jappl_staffclocker_backend.middlewares.jwt_authentication_middleware import JWTTokenAuthentication, JWTTokenSchema
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestJWTTokenAuthenticationMiddleware(TestCase):
    """Test class for JWT token authentication."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Test set up data."""
        user: UserDetail = user_instance.make()
        cls.user_token = RefreshToken.for_user(user=user).access_token
        cls.user_detail: UserDetail = user
        cls.middleware: JWTTokenAuthentication = JWTTokenAuthentication()

    def test_get_user_detail_from_token(self) -> None:
        """Method to test correct token with existing user identity in database."""
        user_detail_result: UserDetail = self.middleware.get_user(validated_token=self.user_token)
        self.assertEqual(user_detail_result.user_id, self.user_detail.user_id)

    def test_get_user_detail_from_token_not_found_user(self) -> None:
        """Method to test correct token with non-existing user identity in database."""
        with self.assertRaises(InvalidToken):
            user_token_with_no_exist_id: AccessToken = self.user_token
            user_token_with_no_exist_id['user_id'] = self.user_detail.user_id + 1
            self.middleware.get_user(validated_token=user_token_with_no_exist_id)

    def test_get_user_detail_from_token_no_user_credential(self) -> None:
        """Method to test correct token with no user identity."""
        with self.assertRaises(InvalidToken):
            user_token_with_no_credential: AccessToken = self.user_token
            user_token_with_no_credential.payload.pop("user_id")
            self.middleware.get_user(validated_token=user_token_with_no_credential)

    def test_jwt_token_schema(self) -> None:
        """Method to test if schema render properly."""
        jwt_token_schema: JWTTokenSchema = JWTTokenSchema(
            target="jappl_staffclocker_backend.middlewares.jwt_authentication_middleware.JWTTokenAuthentication"
        )
        expected_result = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "Bearer",
        }
        self.assertEqual(jwt_token_schema.get_security_definition(_auto_schema="test"), expected_result)
