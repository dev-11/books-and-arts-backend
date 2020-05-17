import unittest
from services import StorageService
from tests.test_environment import mocks
from datetime import datetime as dt

class StorageServiceTests(unittest.TestCase):
    def test_get_returns_empty_json_when_repo_returns_empty_data(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_empty_body())
        result = ss.get('test-key')
        self.assertEqual({}, result)

    def test_get_expiry_date_returns_default_value_for_missing_metadata(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_empty_body())
        result = ss.get_expiry_date('test-key')
        self.assertEqual(dt(2000, 1, 1, 0, 0, 0), result)

    def test_get_secondary_expiry_date_returns_default_value_for_missing_metadata(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_empty_body())
        result = ss.get_secondary_expiry_date('test-key')
        self.assertEqual(dt(2000, 1, 1, 0, 0, 0), result)

    def test_save_or_upate_returns_False_if_repo_cant_save_data(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_empty_body())
        result = ss.save_or_update('', '', '')
        self.assertFalse(result)

    def test_get_expiry_date_returns_expiry_date(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_expiry_date())
        result = ss.get_expiry_date('test-key')
        self.assertEqual(dt.fromisoformat('2020-03-20T14:28:23.382748'), result)       

    def test_get_secondary_expiry_date_returns_expiry_date(self):
        ss = StorageService(mocks.get_mocked_s3repo_returns_expiry_date())
        result = ss.get_secondary_expiry_date('test-key')
        self.assertEqual(dt.fromisoformat('2020-03-21T14:28:23.382748'), result)       
