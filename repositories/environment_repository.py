import os


class EnvironmentRepository:
    def get_parameter(self, parameter_name):
        return os.environ[parameter_name]
