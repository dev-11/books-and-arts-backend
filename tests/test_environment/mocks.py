from unittest.mock import Mock
from repositories import S3Repository


def get_mocked_s3repo_returns_empty_body():
    s3r = S3Repository('')
    s3r.get_body = Mock(name='get_body')
    s3r.get_body.return_value = '{}'
    return s3r