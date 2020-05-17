import unittest
from services import CacheService
from datetime import datetime as dt
from tests.test_environment import mocks


class TestCacheService(unittest.TestCase):
    def test_get_expiry_date_returns_correct_date(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.get_expiry_date('test-key')
        self.assertEqual(dt(2100, 1, 1), result)

    def test_get_secondary_expiry_date_returns_correct_date(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.get_secondary_expiry_date('test-key')
        self.assertEqual(dt(2100, 1, 2), result)

    def test_is_cache_expired_returns_false(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.is_cache_expired('key')
        self.assertFalse(result)

    def test_is_secondary_cache_expired_returns_false(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.is_secondary_cache_expired('key')
        self.assertFalse(result)

    def test_is_cache_expired_returns_true(self):
        cs = CacheService(mocks.get_mocked_storage_service_with_expired_dates())
        result = cs.is_cache_expired('key')
        self.assertTrue(result)

    def test_is_secondary_cache_expired_returns_true(self):
        cs = CacheService(mocks.get_mocked_storage_service_with_expired_dates())
        result = cs.is_secondary_cache_expired('key')
        self.assertTrue(result)
