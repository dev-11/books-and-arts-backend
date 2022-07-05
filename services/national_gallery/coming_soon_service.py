from services import CacheService

from .national_gallery_base_service import (NationalGalleryBaseService,
                                            NationalGalleryScrapingService)


class ComingSoonScrapingService(NationalGalleryScrapingService):
    def __init__(self, url):
        """Scraping the coming soon exhibitions from the url."""
        super().__init__(url)

    def scrape_page(self):
        zipped = super().scrape_page()
        return self.scrape_item_details(zipped[1])


class ComingSoonService(NationalGalleryBaseService):
    def __init__(
        self, scarping_service: ComingSoonScrapingService, cache_service: CacheService
    ):
        """NG coming soon exhibitions service."""
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key)
