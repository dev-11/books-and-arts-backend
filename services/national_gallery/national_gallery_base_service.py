import requests
from bs4 import BeautifulSoup
from services import ServiceStrategy, ScrapingServiceBase
import uuid


class NationalGalleryBaseService(ServiceStrategy):
    def __init__(self, scraping_service, cache_service, key):
        self._scraping_service = scraping_service
        self._key = key
        self._cache_service = cache_service

    def get_service_family_name(self):
        return 'national_gallery'

    def get_data(self, is_hard_get):
        if is_hard_get \
                or self._cache_service.is_cache_expired(self._key) \
                or self._cache_service.get_data(self._key) is None:
            data = self._scraping_service.scrape_page()

            self._cache_service.update_cache(self._key, data, self.get_expiry_date())
            return data

        return self._cache_service.get_data(self._key)


class NationalGalleryScrapingService(ScrapingServiceBase):
    def __init__(self, url):
        self._url = url

    def scrape_item_details(self, divs):
        section = divs[0].find('span').text.strip()
        exhibitions = divs[1].find_all(class_='card exhibition-card')
        e = []
        for _ in exhibitions:
            payment_type = _.find(class_='exhibition-payment-type').text.strip()
            title = _.find(class_='exhibition-title d-flex flex-column').text.strip()
            date = _.find(class_='exhibition-date').text.strip()
            description = _.find(class_='exhibition-description').text.strip()
            img = 'https://www.britishmuseum.org//sites/default/files/styles/1_1_media_tiny/public/2020-01/Arctic_climage_and_culture_british_museum_exhibition_2020.jpg?h=7a45aeb0&itok=ouF4iEZ4%20400w,%20/sites/default/files/styles/1_1_media_small/public/2020-01/Arctic_climage_and_culture_british_museum_exhibition_2020.jpg?h=7a45aeb0&itok=7CsjxhBX%20750w,%20/sites/default/files/styles/1_1_media_medium/public/2020-01/Arctic_climage_and_culture_british_museum_exhibition_2020.jpg'
            # _.find(class_='w-100')

            e.append({
                'id': uuid.uuid4().hex,
                'payment_type': payment_type,
                'title': title,
                'date': date,
                'description': description,
                'img': img
            })

        return {
            'section': section,
            'exhibitions': e
        }

    def scrape_page(self):
        page = requests.get(self._url)

        soup = BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='p-exhibitions-list-view')
        lst2 = lst.find_all(class_='exhibitions-list py-4')
        lst3 = lst.find_all(class_='line-title fluid-line-title')

        zipped = list(zip(lst3, lst2))
        return zipped
