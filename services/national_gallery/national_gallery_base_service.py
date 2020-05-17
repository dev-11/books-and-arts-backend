import requests
from bs4 import BeautifulSoup
from services import ServiceStrategy, ScrapingServiceBase
from hashlib import md5
import cssutils


class NationalGalleryBaseService(ServiceStrategy):
    def __init__(self, scraping_service, cache_service, key):
        """National Gallery base service."""
        self._scraping_service = scraping_service
        self._key = key
        self._cache_service = cache_service

    def get_service_family_name(self):
        return 'national_gallery'

    def get_service_type(self):
        return 'arts'

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
        """General scraping service for NG."""
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
            div_style = _.find(class_='w-100').find('div')['style']
            style = cssutils.parseStyle(div_style)
            url = style['background-image']
            img = url.replace('url(', '').replace(')', '')
            img_url = f'https://www.nationalgallery.org.uk/{img}'

            e.append({
                'id': md5(img_url.encode()).hexdigest(),
                'payment_type': payment_type,
                'title': title,
                'date': date,
                'description': description,
                'img': img_url
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
