from .waterstones_base_service import WaterStonesScrapingService, WaterstonesBaseService
from services import CacheService
import calendar
from datetime import datetime as dt


class BooksOfTheMonthScrapingService(WaterStonesScrapingService):
    def __init__(self, url):
        super().__init__(url)

    def scrape_item_details(self, divs):
        section = divs[0].find('h2').find('em').text.strip()
        title = divs[1].find(class_='title').find('a').text.strip()
        authors = divs[1].find(class_='authors').find('a').text.strip()
        price = divs[1].find('b', itemprop='price').text.strip()
        frmat = divs[1].find(class_='format').text.strip()
        desc = divs[1].find(class_='description').text.strip()
        img = divs[1].div.a.img['src'].replace('/large/', '/medium/')
        return {
            'section': section,
            'title': title,
            'authors': authors,
            'price': price,
            'format': frmat,
            'desc': desc,
            'img': img
        }

    def scrape_page(self):
        sections = super().scrape_page()

        bom = sections[1:]
        grouped = list(zip(*[iter(bom)] * 2))

        data = [self.scrape_item_details(pair) for pair in grouped]
        return data


class BooksOfTheMonthService(WaterstonesBaseService):
    def __init__(self, scarping_service: BooksOfTheMonthScrapingService, cache_service: CacheService):
        key = f'{self.get_service_full_name().replace(".", "/")}.json'
        super().__init__(scarping_service, cache_service, key)

    @staticmethod
    def get_expiry_date():
        today = dt.today()
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        return dt(today.year, today.month, last_day_of_month, 23, 59, 59)
