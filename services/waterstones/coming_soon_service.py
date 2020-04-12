import requests
import bs4
from services import ServiceStrategy


class ComingSoonService(ServiceStrategy):
    def __init__(self, url):
        self._url = url

    def get_service_name(self):
        return "coming_soon"

    @staticmethod
    def get_book_details(divs):
        section = divs[0].find('h2').text.strip()
        bps = divs[0].find_all(class_='book-preview')
        b = []
        for _ in bps:
            title = _.find(class_='title-wrap').text.strip()
            authors = _.find(class_='author-wrap').text.strip()
            price = _.find(class_='price').text.strip()
            b.append({
                'title': title.encode("utf-8"),
                'authors': authors.encode("utf-8"),
                'price': price.encode("utf-8")
            })

        return {
            'section': section.encode("utf-8"),
            'books': b
        }

    def get_data(self):
        page = requests.get(self._url)

        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='row home-row')
        lst2 = lst.find_all(class_='span12')

        bom = lst2[1:]
        grouped = list(zip(*[iter(bom)] * 2))

        return [self.get_book_details(pair) for pair in grouped]
