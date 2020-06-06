import unittest

from services import SecretManagerService
from tests.test_environment import mocks


class TestSecretManagerService(unittest.TestCase):
    def test_get_secret_returns_correct_value(self):
        sms = SecretManagerService(mocks.get_env_repo())
        result = sms.get_secret("asdf")
        self.assertEqual("test_value", result)
