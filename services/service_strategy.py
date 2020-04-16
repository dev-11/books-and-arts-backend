from abc import ABC, abstractmethod


class ServiceStrategy(ABC):
    @abstractmethod
    def get_service_family_name(self):
        pass

    @abstractmethod
    def get_service_name(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

    def get_service_full_name(self):
        return f'{self.get_service_family_name()}.{self.get_service_name()}'
