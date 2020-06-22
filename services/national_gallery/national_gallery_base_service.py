from datetime import datetime as dt
from hashlib import sha256

import cssutils
import requests
from bs4 import BeautifulSoup

from services import ScrapingServiceBase, ServiceStrategy


class NationalGalleryBaseService(ServiceStrategy):
    def __init__(self, scraping_service, cache_service, key):
        """National Gallery base service."""
        self._scraping_service = scraping_service
        self._key = key
        self._cache_service = cache_service

    def get_service_family_name(self):
        return "national_gallery"

    def get_service_type(self):
        return "arts"

    def is_cache_expired(self):
        update_date = self._cache_service.get_cache_update_date(self._key)
        return update_date + self.get_service_life() <= dt.now()

    def get_data(self, is_hard_get, is_auto_refresh):
        if (
            is_hard_get
            or (self.is_cache_expired() and is_auto_refresh)
            or self._cache_service.get_data(self._key) is None
        ):
            data = self._scraping_service.scrape_page()

            self._cache_service.update_cache(self._key, data, dt.now())
            return data

        return self._cache_service.get_data(self._key)


class NationalGalleryScrapingService(ScrapingServiceBase):
    def __init__(self, url):
        """General scraping service for NG."""
        self._url = url

    def scrape_item_details(self, divs):
        section = divs[0].find("span").text.strip()
        exhibitions = divs[1].find_all(class_="card exhibition-card")
        e = []
        for _ in exhibitions:
            payment_type = _.find(class_="exhibition-payment-type").text.strip()
            title = _.find(class_="exhibition-title d-flex flex-column").text.strip()
            date = _.find(class_="exhibition-date").text.strip()
            description = _.find(class_="exhibition-description").text.strip()
            div_style = _.find(class_="w-100").find("div")["style"]
            style = cssutils.parseStyle(div_style)
            url = style["background-image"]
            img = url.replace("url(", "").replace(")", "")
            img_url = f"https://www.nationalgallery.org.uk/{img}"

            e.append(
                {
                    "id": sha256(img_url.encode()).hexdigest(),
                    "payment_type": payment_type,
                    "title": title,
                    "date": date,
                    "description": description,
                    "img": img_url,
                }
            )

        return {"section": section, "exhibitions": e}

    def scrape_page(self):
        page = requests.get(self._url)

        soup = BeautifulSoup(page.text, "html.parser")

        lst = soup.find(class_="p-exhibitions-list-view")
        lst2 = lst.find_all(class_="exhibitions-list py-4")
        lst3 = lst.find_all(class_="line-title")

        zipped = list(zip(lst3, lst2))
        return zipped
