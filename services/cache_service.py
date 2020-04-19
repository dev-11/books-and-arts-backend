from repositories import S3Repository
from datetime import datetime as dt
from datetime import timedelta as td


class CacheService:
    def __init__(self, repository: S3Repository):
        self._repository = repository

    def set_key(self, key):
        pass

    def get_expiry_date(self, key):
        metadata = self._repository.get_metadata(key)
        try:
            return metadata['expiry_date']
        except KeyError:
            return None

    def get_data(self, key):
        return self._repository.get_body(key)

    def update_cache(self, key, data, service_life_in_seconds):
        expiry_date = dt.now() + td(seconds=service_life_in_seconds)
        self._repository.save_or_update_file(key, data, expiry_date)

    def is_cache_expired(self, key):
        return self.get_expiry_date(key) <= dt.now()
