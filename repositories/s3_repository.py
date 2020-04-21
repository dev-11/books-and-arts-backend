import boto3
from botocore.errorfactory import ClientError


class S3Repository:
    def __init__(self, bucket):
        self._bucket = bucket
        self._s3 = boto3.resource('s3')

    def get_body(self, key):
        obj = self._s3.Object(self._bucket, key)
        body = obj.get()['Body'].read()
        return body

    def get_metadata(self, key):
        obj = self._s3.Object(self._bucket, key)
        metadata = obj.get()['Metadata']
        return metadata

    def has_key(self, key):
        try:
            self._s3.Bucket(self._bucket).Object(key).last_modified
        except ClientError:
            return False
        return True

    def save_or_update_file(self, key, body, expiry_date):
        try:
            obj = self._s3.Object(self._bucket, key)
            obj.put(Body=body, Metadata={'expiry-date': str(expiry_date)})

        except ClientError as e:
            return False
        return True
