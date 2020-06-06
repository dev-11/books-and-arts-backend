import requests
from bs4 import BeautifulSoup

from services import CacheService

from .national_gallery_base_service import (NationalGalleryBaseService,
                                            NationalGalleryScrapingService)


class CurrentExhibitionsScrapingService(NationalGalleryScrapingService):
    def __init__(self, url):
        """Getting the currently running exhibitions of the url."""
        super().__init__(url)

    def scrape_page(self):
        page = requests.get(self._url)

        soup = BeautifulSoup(page.text, "html.parser")

        lst = soup.find(class_="p-exhibitions-list-view")
        lst2 = lst.find_all(class_="exhibitions-list py-4")
        lst3 = lst.find_all(class_="line-title fluid-line-title")

        zipped = list(zip(lst3, lst2))
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
