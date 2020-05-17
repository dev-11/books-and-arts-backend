import unittest
from services import CacheService
from datetime import datetime as dt
from tests.test_environment import mocks


class TestCacheService(unittest.TestCase):
    def test_01(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.get_expiry_date('test-key')
        self.assertEqual(dt(2100, 1, 1), result)

    def test_02(self):
        cs = CacheService(mocks.get_mocked_storage_service())
        result = cs.get_secondary_expiry_date('test-key')
        self.assertEqual(dt(2100, 1, 2), result)
