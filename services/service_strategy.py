from abc import ABC, abstractmethod
import config


class ServiceStrategy(ABC):
    @abstractmethod
    def get_service_family_name(self):
        pass

    def get_service_name(self):
        service_name = self.__class__.__name__.replace('Service', '')

        return ''.join(['_' + i.lower() if i.isupper()
                        else i for i in service_name]).lstrip('_')

    @abstractmethod
    def get_data(self):
        pass

    def get_service_full_name(self):
        return f'{self.get_service_family_name()}.{self.get_service_name()}'

    @staticmethod
    def get_service_life_in_seconds():
        return config.default_service_life_in_seconds

