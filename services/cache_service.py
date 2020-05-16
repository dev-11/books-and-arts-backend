from datetime import datetime as dt
from services import StorageService


class CacheService:
    def __init__(self, storage_service: StorageService):
        self._storage_service = storage_service

    def get_expiry_date(self, key):
        return self._storage_service.get_expiry_date(key)

    def get_data(self, key):
        return self._storage_service.get(key)

    def update_cache(self, key, data, expiry_date, secondary_expiry_date = None):
        self._storage_service.save_or_update(key, data, expiry_date, secondary_expiry_date)

    def is_cache_expired(self, key):
        return self.get_expiry_date(key) <= dt.now()

    def is_secondary_cache_expired(self, key):
        return self.get_secondary_expiry_date(key) <= dt.now()

    def get_secondary_expiry_date(self, key):
        return self._storage_service.get_secondary_expiry_date(key)
