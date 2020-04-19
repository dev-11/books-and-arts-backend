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
            self._s3.head_object(Bucket=self._bucket, Key=key)
        except ClientError:
            return False
        return True

    def save_or_update_file(self, key, value, expiry_date):
        try:
            obj = self._s3.Object(self._bucket, key)
            obj.put(Body=value, ExtraArgs={'Metadata': {'expiry_date': expiry_date}})

        except ClientError as e:
            return False
        return True
