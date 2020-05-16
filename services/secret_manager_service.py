from repositories.secret_repository import SecretRepository


class SecretManagerService:
    def __init__(self, secret_repository: SecretRepository):
        self._secret_repository = secret_repository

    def get_secret(self, secret_name):
        return self._secret_repository.get_parameter(secret_name)
