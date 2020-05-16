import os


class SecretRepository:
    def get_parameter(self, parameter_name):
        pass


class SSMRepository(SecretRepository):
    def get_parameter(self, parameter_name):
        return os.environ[parameter_name]


class LocalSecretRepository(SecretRepository):
    def get_parameter(self, parameter_name):
        return os.environ[parameter_name]
