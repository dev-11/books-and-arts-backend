from unittest.mock import Mock
from repositories import S3Repository
from services import StorageService
from datetime import datetime as dt


def get_mocked_s3repo_returns_empty_body():
    s3r = S3Repository('test- bucket')
    s3r.get_body = Mock(name='get_body')
    s3r.get_body.return_value = '{}'
    s3r.get_metadata = Mock(name='get_metadata')
    s3r.get_metadata.return_value = ''
    s3r.has_key = Mock(name='has_key')
    s3r.has_key.return_value = False
    s3r.save_or_update_file = Mock(name='save_or_update_file')
    s3r.save_or_update_file.return_value = False
    return s3r

def get_mocked_s3repo_returns_expiry_date():
    s3r = S3Repository('test- bucket')
    s3r.get_metadata = Mock(name='get_metadata')
    s3r.get_metadata.return_value = {
        'expiry-date': '2020-03-20T14:28:23.382748',
        'secondary-expiry-date': '2020-03-21T14:28:23.382748'
    }
    s3r.has_key = Mock(name='has_key')
    s3r.has_key.return_value = True
    return s3r

def get_mocked_storage_service():
    ss = StorageService(None)
    ss.get_expiry_date = Mock(name='get_expiry_date')
    ss.get_expiry_date.return_value = dt(2100, 1, 1)
    ss.get_secondary_expiry_date = Mock(name='get_secondary_expiry_date')
    ss.get_secondary_expiry_date.return_value = dt(2100, 1, 2)
    return ss
