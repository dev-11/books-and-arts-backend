import boto3


class S3Repository:
    def __init__(self, bucket):
        self._bucket = bucket
        self._s3 = boto3.resource('s3')

    def read(self, file):
        obj = self._s3.Object(self._bucket, file)
        body = obj.get()['Body'].read()
        return body
