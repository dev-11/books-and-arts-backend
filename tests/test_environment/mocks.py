from datetime import datetime as dt
from unittest.mock import Mock

from repositories import EnvironmentRepository, S3Repository
from services import StorageService


def get_mocked_s3repo_returns_empty_body():
    s3r = S3Repository("test- bucket")
    s3r.get_body = Mock(name="get_body")
    s3r.get_body.return_value = "{}"
    s3r.get_metadata = Mock(name="get_metadata")
    s3r.get_metadata.return_value = ""
    s3r.has_key = Mock(name="has_key")
    s3r.has_key.return_value = False
    s3r.save_or_update_file = Mock(name="save_or_update_file")
    s3r.save_or_update_file.return_value = False
    return s3r


def get_mocked_s3repo_has_key_but_no_metadata():
    s3r = S3Repository("test- bucket")
    s3r.get_body = Mock(name="get_body")
    s3r.get_body.return_value = "{}"
    s3r.get_metadata = Mock(name="get_metadata")
    s3r.get_metadata.return_value = {}
    s3r.has_key = Mock(name="has_key")
    s3r.has_key.return_value = True
    s3r.save_or_update_file = Mock(name="save_or_update_file")
    s3r.save_or_update_file.return_value = False
    return s3r


def get_mocked_s3repo_returns_cache_update_date():
    s3r = S3Repository("test- bucket")
    s3r.get_metadata = Mock(name="get_metadata")
    s3r.get_metadata.return_value = {
        "cache-update-date": "2020-03-20T14:28:23.382748",
    }
    s3r.has_key = Mock(name="has_key")
    s3r.has_key.return_value = True
    return s3r


def get_mocked_storage_service():
    ss = StorageService(None)
    ss.get_cache_update_date = Mock(name="get_cache_update_date")
    ss.get_cache_update_date.return_value = dt(2020, 1, 10)
    ss.get = Mock(name="get")
    ss.get.return_value = "asdf"
    ss.save_or_update = Mock(name="save_or_update")
    ss.save_or_update.result_value = True
    return ss


def get_env_repo():
    er = EnvironmentRepository()
    er.get_parameter = Mock(name="get_parameter")
    er.get_parameter.return_value = "test_value"
    return er
