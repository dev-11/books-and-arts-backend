import boto3
import os


class SecretRepository:
    def get_parameter(self, parameter_name):
        pass


class SSMRepository(SecretRepository):
    def __init__(self):
        self._ssm = boto3.resource('ssm')

    def get_parameter(self, parameter_name):
        return self._ssm.get_parameter(parameter_name)


class LocalSecretRepository(SecretRepository):
    def get_parameter(self, parameter_name):
        return os.environ[parameter_name]
