import requests
import bs4
from services import ServiceStrategy


class ComingSoonService(ServiceStrategy):
    def __init__(self, url):
        self._url = url

    def get_service_family_name(self):
        return 'waterstones'

    @staticmethod
    def get_book_details(divs):
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

    def get_data(self):
        page = requests.get(self._url)

        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='row home-row')
        lst2 = lst.find_all(class_='span12')

        bom = lst2[1:]
        bom.pop(1)  # removing 'special' section

        return [self.get_book_details(pair) for pair in bom]
