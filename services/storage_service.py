from repositories.s3_repository import S3Repository
from datetime import datetime as dt
import json


class StorageService:
    def __init__(self, repo: S3Repository):
        self._repo = repo

    def get_expiry_date(self, key):
        if self._repo.has_key(key):
            metadata = self._repo.get_metadata(key)
            return dt.fromisoformat(metadata['expiry-date'])

        return dt(2000, 1, 1, 0, 0, 0)

    def get_secondary_expiry_date(self, key):
        if self._repo.has_key(key):
            metadata = self._repo.get_metadata(key)
            return dt.fromisoformat(metadata['secondary-expiry-date'])

        return dt(2000, 1, 1, 0, 0, 0)

    def get(self, key):
        data = self._repo.get_body(key)
        return json.loads(data)

    def save_or_update(self, key, data, expiry_date, secondary_expiry_date = None):
        return self._repo.save_or_update_file(key, json.dumps(data), expiry_date, secondary_expiry_date)
