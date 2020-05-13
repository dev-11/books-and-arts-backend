from services import ServiceStrategy, ScrapingServiceBase
import requests
import bs4
import hashlib


class WaterstonesBaseService(ServiceStrategy):
    def __init__(self, scraping_service, cache_service, key):
        self._scraping_service = scraping_service
        self._key = key
        self._cache_service = cache_service

    def get_service_family_name(self):
        return 'waterstones'

    def get_service_type(self):
        return 'books'

    def get_data(self, is_hard_get):
        if is_hard_get \
                or self._cache_service.is_cache_expired(self._key) \
                or self._cache_service.get_data(self._key) is None:
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
            img = _.find(class_='image-wrap').a.img['data-src'].replace('/large/', '/medium/')
            book_url = f"https://www.waterstones.com/{_.find(class_='image-wrap').a['href']}"
            genres, nop, published_at, desc = self.get_extra(book_url)
            books.append({
                'id': hashlib.md5(book_url.encode()).hexdigest(),
                'title': title,
                'authors': authors,
                'price': price,
                'format': frmt,
                'img': img,
                'genres': genres,
                'number_of_pages': nop,
                'published_at': published_at,
                'desc': desc
            })

        return {
            'section': section,
            'books': books
        }

    def get_extra(self, link):
        page = requests.get(link)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        genre = soup.find(class_="breadcrumbs span12")

        genres = [_.text for _ in genre.findAll('a')]
        number_of_pages = self.get_text_or_default(soup.find(itemprop="numberOfPages")).strip()
        date_published = self.get_text_or_default(soup.find(itemprop="datePublished")).strip()
        description = soup.find("div", id="scope_book_description").text.strip()

        return genres, number_of_pages, date_published, description

    @staticmethod
    def get_text_or_default(html_tag: bs4.PageElement):
        return 'N/A' if html_tag is None else html_tag.text.strip()

    def scrape_page(self):
        page = requests.get(self._url)

        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='row home-row')
        lst2 = lst.find_all(class_='span12')
        return lst2
