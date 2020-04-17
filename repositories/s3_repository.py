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
        head = self._s3.head_object(Bucket=self._bucket, Key=key)
        return head['Metadata']

    def has_key(self, key):
        try:
            self._s3.head_object(Bucket=self._bucket, Key=key)
        except ClientError:
            return False
        return True
