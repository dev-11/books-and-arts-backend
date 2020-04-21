from .waterstones_base_service import WaterstonesBaseService, ScrapingServiceBase
from services import CacheService


class NewBooksScrapingService(ScrapingServiceBase):
    def __init__(self, url):
        self._url = url

    def scrape_item_details(self, divs):
        super().scrape_item_details(divs)

    def scrape_page(self):
        lst2 = super().scrape_page()

        bom = lst2[1:7]
        bom.pop(2)  # removing 'special' section

        return [self.scrape_item_details(pair) for pair in bom]


class NewBooksService(WaterstonesBaseService):
    def __init__(self, scarping_service: NewBooksScrapingService, cache_service: CacheService):
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key)
