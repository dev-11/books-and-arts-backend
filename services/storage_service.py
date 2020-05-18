from repositories.s3_repository import S3Repository
from datetime import datetime as dt
import json


class StorageService:
    def __init__(self, repo: S3Repository):
        """Service to store/read data."""
        self._repo = repo

    def get_cache_update_date(self, key):
        if self._repo.has_key(key):
            metadata = self._repo.get_metadata(key)
            if 'cache-update-date' not in metadata:
                return dt(2000, 1, 1, 0, 0, 0)
            return dt.fromisoformat(metadata['cache-update-date'])

        return dt(2000, 1, 1, 0, 0, 0)

    def get(self, key):
        data = self._repo.get_body(key)
        return json.loads(data)

    def save_or_update(self, key, data, cache_udpate_date):
        return self._repo.save_or_update_file(key, json.dumps(data), cache_udpate_date)
