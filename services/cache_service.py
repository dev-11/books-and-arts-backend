from repositories import S3Repository
from datetime import datetime as dt
from datetime import timedelta as td


class CacheService:
    def __init__(self, repository: S3Repository):
        self._repository = repository

    def get_expiry_date(self, key):
        if self._repository.has_key(key):
            metadata = self._repository.get_metadata(key)
            return metadata['expiry-date']

        return dt(2000, 1, 1, 0, 0, 0)

    def get_data(self, key):
        return self._repository.get_body(key)

    def update_cache(self, key, data, service_life_in_seconds):
        expiry_date = dt.now() + td(seconds=service_life_in_seconds)
        self._repository.save_or_update_file(key, data, expiry_date)

    def is_cache_expired(self, key):
        return dt.fromisoformat(self.get_expiry_date(key)) <= dt.now()
