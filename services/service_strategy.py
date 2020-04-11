from abc import ABC, abstractmethod


class ServiceStrategy(ABC):
    @abstractmethod
    def get_service_name(self):
        pass

    @abstractmethod
    def get_data(self):
        pass