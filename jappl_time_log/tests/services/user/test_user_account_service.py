from django.test import TestCase

from jappl_time_log.dataclasses.user.login_input_dataclass import LoginInputDataclass
from jappl_time_log.models.user_detail_model import UserDetail
from jappl_time_log.services.user.user_account_service import UserAccountService
from jappl_time_log.tests.model_instances.user_detail_instance import user_instance


class TestUserAccountService(TestCase):
    """Test class for service related to authentication."""

    @classmethod
    def setUpTestData(cls):
        """Mock user data for test case."""
        cls.user: UserDetail = user_instance.make(email="test@gmail.com")

    def test_generate_token_invalid_hash_password(self):
        """Method to test password is in incorrect hash format."""
        user_input: LoginInputDataclass = LoginInputDataclass(email=self.user.email, password=self.user.password)
        token, user_detail = UserAccountService.generate_token(user_input)
        self.assertEqual(token, "")
        self.assertEqual(user_detail, None)
