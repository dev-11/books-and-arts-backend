from abc import ABC, abstractmethod
from datetime import timedelta as td
import config


class ServiceStrategy(ABC):
    @abstractmethod
    def get_service_type(self):
        pass

    @abstractmethod
    def get_service_family_name(self):
        pass

    def get_service_name(self):
        service_name = self.__class__.__name__.replace('Service', '')

        return ''.join(['_' + i.lower() if i.isupper()
                        else i for i in service_name]).lstrip('_')

    @abstractmethod
    def get_data(self, is_hard_get):
        pass

    def get_service_full_name(self):
        return f'{self.get_service_family_name()}.{self.get_service_name()}'

    @staticmethod
    def get_service_life():
        return td(seconds=config.default_service_life_in_seconds)

    @abstractmethod
    def is_cache_expired(self):
        pass

class ScrapingServiceBase(ABC):
    @abstractmethod
    def scrape_page(self):
        pass

    @abstractmethod
    def scrape_item_details(self, divs):
        pass
