import uuid
from datetime import datetime as dt

import bs4
import requests

from services import CacheService

from .merging_service import MergingService
from .waterstones_base_service import (WaterstonesBaseService,
                                       WaterStonesScrapingService)


class BooksOfTheMonthScrapingService(WaterStonesScrapingService):
    def __init__(self, url):
        """Scraping the books of the months."""
        super().__init__(url)

    @staticmethod
    def get_section(h2):
        em = h2.find("em")
        return (em if em is not None else h2).text.strip()

    def scrape_item_details(self, divs):
        section = self.get_section(divs[0].find("h2"))
        title = divs[1].find(class_="title").find("a").text.strip()
        authors = divs[1].find(class_="authors").find("a").text.strip()
        price = divs[1].find("b", itemprop="price").text.strip()
        frmat = divs[1].find(class_="format").text.strip()
        desc = divs[1].find(class_="description").text.strip()
        img = divs[1].div.a.img["src"].replace("/large/", "/medium/")
        genres, nop, published_at, isbn = self.get_extra(
            f'https://www.waterstones.com/{divs[1].div.a["href"]}'
        )

        return {
            "section": section,
            "books": [
                {
                    "id": uuid.uuid4().hex,
                    "title": title,
                    "authors": authors,
                    "price": price,
                    "format": frmat,
                    "desc": desc,
                    "img": img,
                    "genres": genres,
                    "number_of_pages": nop,
                    "published_at": published_at,
                    "isbn": isbn,
                }
            ],
        }

    @staticmethod
    def get_extra(link):
        page = requests.get(link)
        soup = bs4.BeautifulSoup(page.text, "html.parser")

        genre = soup.find(class_="breadcrumbs span12")

        genres = list(set([_.text for _ in genre.findAll("a")]))
        number_of_pages = soup.find(itemprop="numberOfPages").text.strip()
        date_published = soup.find(itemprop="datePublished").text.strip()
        isbn = soup.find(itemprop="isbn").text.strip()

        return genres, number_of_pages, date_published, isbn

    def scrape_page(self):
        sections = super().scrape_page()

        bom = sections[1:]
        grouped = list(zip(*[iter(bom)] * 2))

        data = [self.scrape_item_details(pair) for pair in grouped]
        return data


class BooksOfTheMonthService(WaterstonesBaseService):
    def __init__(
        self,
        scarping_service: BooksOfTheMonthScrapingService,
        cache_service: CacheService,
        merging_service: MergingService,
    ):
        """Books of the month service."""
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key, merging_service)

    def is_cache_expired(self):
        update_date = self._cache_service.get_cache_update_date(self._key)
        today = dt.now()
        first_day_of_month = dt(today.year, today.month, 1, 0, 0, 0)
        return update_date <= first_day_of_month
