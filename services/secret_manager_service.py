from repositories.environment_repository import EnvironmentRepository


class SecretManagerService:
    def __init__(self, repository: EnvironmentRepository):
        self._repository = repository

    def get_secret(self, secret_name):
        return self._repository.get_parameter(secret_name)
