from services import StorageService


class CacheService:
    def __init__(self, storage_service: StorageService):
        """Cache service."""
        self._storage_service = storage_service

    def get_cache_update_date(self, key):
        return self._storage_service.get_cache_update_date(key)

    def get_data(self, key):
        return self._storage_service.get(key)

    def update_cache(self, key, data, update_date):
        return self._storage_service.save_or_update(key, data, update_date)
