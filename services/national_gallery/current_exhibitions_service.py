from services import CacheService

from .national_gallery_base_service import (NationalGalleryBaseService,
                                            NationalGalleryScrapingService)


class CurrentExhibitionsScrapingService(NationalGalleryScrapingService):
    def __init__(self, url):
        """Getting the currently running exhibitions of the url."""
        super().__init__(url)

    def scrape_page(self):
        zipped = super().scrape_page()
        return self.scrape_item_details(zipped[0])


class CurrentExhibitionsService(NationalGalleryBaseService):
    def __init__(
        self,
        scarping_service: CurrentExhibitionsScrapingService,
        cache_service: CacheService,
    ):
        """NG service to get current services."""
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key)
