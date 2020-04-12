import requests
import bs4
from services import ServiceStrategy


class ComingSoonService(ServiceStrategy):
    def __init__(self, url):
        self._url = url

    def get_service_name(self):
        return "coming_soon_service"

    @staticmethod
    def get_book_details(divs):
        section = divs[0].find('h2').text.strip()
        bp = divs[0].find(class_='book-preview')
        title = bp.find(class_='title-wrap').text.strip()
        authors = bp.find(class_='author-wrap').text.strip()
        price = bp.find(class_='price').text.strip()
        return {
            'section': section.encode("utf-8"),
            'title': title.encode("utf-8"),
            'authors': authors.encode("utf-8"),
            'price': price.encode("utf-8")
        }

    def get_data(self):
        page = requests.get(self._url)

        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='row home-row')
        lst2 = lst.find_all(class_='span12')

        bom = lst2[1:]
        grouped = list(zip(*[iter(bom)] * 2))

        return [self.get_book_details(pair) for pair in grouped]
