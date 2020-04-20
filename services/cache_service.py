from datetime import datetime as dt
from services import StorageService


class CacheService:
    def __init__(self, storage_service: StorageService):
        self._storage_service = storage_service

    def get_expiry_date(self, key):
        return self._storage_service.get_expiry_date(key)

    def get_data(self, key):
        return self._storage_service.get(key)

    def update_cache(self, key, data, expiry_date):
        self._storage_service.save_or_update(key, data, expiry_date)

    def is_cache_expired(self, key):
        return dt.fromisoformat(self.get_expiry_date(key)) <= dt.now()
