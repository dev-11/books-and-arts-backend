from .waterstones_base_service import WaterStonesScrapingService, WaterstonesBaseService
from services import CacheService


class ComingSoonScrapingService(WaterStonesScrapingService):
    def __init__(self, url):
        super().__init__(url)

    def scrape_page(self):
        lst2 = super().scrape_page()

        bom = lst2[1:]
        bom.pop(1)  # removing 'special' section

        return [self.scrape_item_details(pair) for pair in bom]


class ComingSoonService(WaterstonesBaseService):
    def __init__(self, scarping_service: ComingSoonScrapingService, cache_service: CacheService):
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key)
