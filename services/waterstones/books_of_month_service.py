from .waterstones_base_service import InnerService
from repositories import S3Repository
import json
import config


class BooksOfTheMonthService(InnerService):
    def __init__(self, url):
        self._url = url

    @staticmethod
    def get_book_details(divs):
        section = divs[0].find('h2').find('em').text.strip()
        title = divs[1].find(class_='title').find('a').text.strip()
        authors = divs[1].find(class_='authors').find('a').text.strip()
        price = divs[1].find('b', itemprop='price').text.strip()
        frmat = divs[1].find(class_='format').text.strip()
        desc = divs[1].find(class_='description').text.strip()
        img = divs[1].div.a.img['src']
        return {
            'section': section,
            'title': title,
            'authors': authors,
            'price': price,
            'format': frmat,
            'desc': desc,
            'img': img
        }

    def get_data(self):
        # lst2 = super().get_data()
        #
        # bom = lst2[1:]
        # grouped = list(zip(*[iter(bom)] * 2))
        #
        # return [self.get_book_details(pair) for pair in grouped]
        s3r = S3Repository(config.data_bucket)
        key = f'{self.get_service_family_name()}/{self.get_service_name()}.json'
        # data = s3r.read_body(key)
        data = s3r.get_metadata(key)
        return json.loads(data)
