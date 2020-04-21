from services import ServiceStrategy, ScrapingServiceBase
import requests
import bs4


class WaterstonesBaseService(ServiceStrategy):
    def __init__(self, scraping_service, cache_service, key):
        self._scraping_service = scraping_service
        self._key = key
        self._cache_service = cache_service

    def get_service_family_name(self):
        return 'waterstones'

    def get_data(self):
        if self._cache_service.is_cache_expired(self._key) or self._cache_service.get_data(self._key) is None:

            data = self._scraping_service.scrape_page()

            self._cache_service.update_cache(self._key, data, self.get_expiry_date())
            return data

        return self._cache_service.get_data(self._key)


class WaterStonesScrapingService(ScrapingServiceBase):

    def __init__(self, url):
        self._url = url

    def scrape_item_details(self, divs):
        section = divs.find('h2').text.strip()
        book_previews = divs.find_all(class_='book-preview')
        books = []
        for _ in book_previews:
            title = _.find(class_='title-wrap').text.strip()
            authors = _.find(class_='author-wrap').text.strip()
            price = _.find(class_='price').text.strip()
            frmt = _.find(class_='format').text.strip()
            img = _.find(class_='image-wrap').a.img['data-src']
            books.append({
                'title': title.encode("utf-8"),
                'authors': authors.encode("utf-8"),
                'price': price.encode("utf-8"),
                'format': frmt.encode("utf-8"),
                'img': img.encode("utf-8")
            })

        return {
            'section': section.encode("utf-8"),
            'books': books
        }

    def scrape_page(self):
        page = requests.get(self._url)

        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='row home-row')
        lst2 = lst.find_all(class_='span12')
        return lst2
