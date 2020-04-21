from .waterstones_base_service import ScrapingServiceBase, WaterstonesBaseService
from services import CacheService


class ComingSoonScrapingService(ScrapingServiceBase):
    def __init__(self, url):
        self._url = url

    def scrape_item_details(self, divs):
        return super().scrape_item_details(divs)

    def scrape_page(self):
        lst2 = super().scrape_page()

        bom = lst2[1:]
        bom.pop(1)  # removing 'special' section

        return [self.scrape_item_details(pair) for pair in bom]


class ComingSoonService(WaterstonesBaseService):
    def __init__(self, scarping_service: ComingSoonScrapingService, cache_service: CacheService):
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key)
