from repositories import EnvironmentRepository


class SecretManagerService:
    def __init__(self, repository: EnvironmentRepository):
        """Service to manage secrets."""
        self._repository = repository

    def get_secret(self, secret_name):
        return self._repository.get_parameter(secret_name)
