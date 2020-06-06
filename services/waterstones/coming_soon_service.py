from services import CacheService

from .merging_service import MergingService
from .waterstones_base_service import WaterstonesBaseService, WaterStonesScrapingService


class ComingSoonScrapingService(WaterStonesScrapingService):
    def __init__(self, url):
        """Scraping the coming soon section of the url."""
        super().__init__(url)

    def scrape_page(self):
        lst2 = super().scrape_page()

        bom = lst2[1:]
        bom.pop(1)  # removing 'special' section

        return [self.scrape_item_details(pair) for pair in bom]


class ComingSoonService(WaterstonesBaseService):
    def __init__(
        self,
        scarping_service: ComingSoonScrapingService,
        cache_service: CacheService,
        merging_service: MergingService,
    ):
        """Service to handle the coming soon books."""
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key, merging_service)
