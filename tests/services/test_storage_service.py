import unittest
from services import StorageService
from tests.test_environment import mocks


class StorageServiceTests(unittest.TestCase):
    def test_get_returns_empty_json_when_repo_returns_empty_data(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_empty_body())
        result = ss.get('test-key')
        self.assertEqual({}, result)
