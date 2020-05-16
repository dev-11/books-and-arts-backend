import boto3
from secrets import secrets


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
        return secrets[parameter_name]
