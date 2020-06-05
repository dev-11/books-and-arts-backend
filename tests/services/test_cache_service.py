import unittest
from services import CacheService
from datetime import datetime as dt
from tests.test_environment import mocks


class TestCacheService(unittest.TestCase):
    def test_get_cache_update_date_returns_correct_date(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.get_cache_update_date("test-key")
        self.assertEqual(dt(2020, 1, 10), result)

    def test_get_data_returns_unchanged_data(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.get_data("key")
        self.assertEqual("asdf", result)

    def test_update_cache_returns_true(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.update_cache("", "", "")
        self.assertTrue(result)
