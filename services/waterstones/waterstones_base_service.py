from datetime import datetime as dt
from datetime import timedelta as td
from hashlib import sha256

import bs4
import requests

from services import CacheService, ScrapingServiceBase, ServiceStrategy

from .merging_service import MergingService


class WaterstonesBaseService(ServiceStrategy):
    def __init__(
        self,
        scraping_service,
        cache_service: CacheService,
        key,
        merging_service: MergingService,
    ):
        """Base service."""
        self._scraping_service = scraping_service
        self._key = key
        self._cache_service = cache_service
        self._merging_service = merging_service

    def get_service_family_name(self):
        return "waterstones"

    def get_service_type(self):
        return "books"

    def is_cache_expired(self):
        update_date = self._cache_service.get_cache_update_date(self._key)
        return update_date + self.get_service_life() <= dt.now()

    def is_secondary_cache_expired(self):
        update_date = self._cache_service.get_cache_update_date(self._key)
        return update_date + self.get_secondary_service_life() <= dt.now()

    @staticmethod
    def get_secondary_service_life():
        return td(days=1)

    def get_data(self, is_hard_get, is_auto_refresh):
        if (
            is_hard_get
            or (self.is_cache_expired() and is_auto_refresh)
            or self._cache_service.get_data(self._key) is None
        ):
            data = self._scraping_service.scrape_page()

            isbns = self.get_isbns(data)
            data = self._merging_service.merge(data, isbns)

            self._cache_service.update_cache(self._key, data, dt.now())
            return data

        data = self._cache_service.get_data(self._key)
        if self.is_secondary_cache_expired():
            isbns = self.get_isbns(data)
            data = self._merging_service.merge(data, isbns)
            self._cache_service.update_cache(self._key, data, dt.now())
            return data

        return data

    def get_isbns(self, sections):
        return [book["isbn"] for section in sections for book in section["books"]]


class WaterStonesScrapingService(ScrapingServiceBase):
    def __init__(self, url):
        """General scraping service."""
        self._url = url

    def scrape_item_details(self, divs):
        section = divs.find("h2").text.strip()
        book_previews = divs.find_all(class_="book-preview")
        books = []
        for _ in book_previews:
            title = _.find(class_="title-wrap").text.strip()
            authors = _.find(class_="author-wrap").text.strip()
            price = _.find(class_="price").text.strip()
            frmt = _.find(class_="format").text.strip()
            img = (
                _.find(class_="image-wrap")
                .a.img["data-src"]
                .replace("/large/", "/medium/")
            )
            book_url = (
                f"https://www.waterstones.com/{_.find(class_='image-wrap').a['href']}"
            )
            genres, nop, published_at, isbn, desc = self.get_extra(book_url)
            books.append(
                {
                    "id": sha256(book_url.encode()).hexdigest(),
                    "title": title,
                    "authors": authors,
                    "price": price,
                    "format": frmt,
                    "img": img,
                    "genres": genres,
                    "number_of_pages": nop,
                    "published_at": published_at,
                    "isbn": isbn,
                    "desc": desc,
                }
            )

        return {"section": section, "books": books}

    def get_extra(self, link):
        page = requests.get(link)
        soup = bs4.BeautifulSoup(page.text, "html.parser")

        genre = soup.find(class_="breadcrumbs span12")

        genres = list(set([_.text for _ in genre.findAll("a")]))
        number_of_pages = self.get_text_or_default(
            soup.find(itemprop="numberOfPages")
        ).strip()
        isbn = self.get_text_or_default(soup.find(itemprop="isbn")).strip()
        date_published = self.get_text_or_default(
            soup.find(itemprop="datePublished")
        ).strip()
        description = soup.find("div", id="scope_book_description").text.strip()

        return genres, number_of_pages, date_published, isbn, description

    @staticmethod
    def get_text_or_default(html_tag: bs4.PageElement):
        return "" if html_tag is None else html_tag.text.strip()

    def scrape_page(self):
        page = requests.get(self._url)

        soup = bs4.BeautifulSoup(page.text, "html.parser")

        lst = soup.find(class_="row home-row")
        lst2 = lst.find_all(class_="span12")
        return lst2
