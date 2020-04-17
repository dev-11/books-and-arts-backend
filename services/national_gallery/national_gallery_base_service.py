import requests
from bs4 import BeautifulSoup
from services import ServiceStrategy


class NationalGalleryBaseService(ServiceStrategy):
    def get_service_family_name(self):
        return 'national_gallery'


class InnerService(NationalGalleryBaseService):
    @staticmethod
    def get_exhibition_details(divs):
        section = divs[0].find('span').text.strip()
        exhibitions = divs[1].find_all(class_='card exhibition-card')
        e = []
        for _ in exhibitions:
            payment_type = _.find(class_='exhibition-payment-type').text.strip()
            title = _.find(class_='exhibition-title d-flex flex-column').text.strip()
            date = _.find(class_='exhibition-date').text.strip()
            description = _.find(class_='exhibition-description').text.strip()
            img = _.find(class_='w-100')

            e.append({
                'payment_type': payment_type.encode("utf-8"),
                'title': title.encode("utf-8"),
                'date': date.encode("utf-8"),
                'description': description.encode("utf-8"),
                'img': img.encode("utf-8")
            })

        return {
            'section': section,
            'exhibitions': e
        }

    def get_data(self):
        page = requests.get(self._url)

        soup = BeautifulSoup(page.text, 'html.parser')

        lst = soup.find(class_='p-exhibitions-list-view')
        lst2 = lst.find_all(class_='exhibitions-list py-4')
        lst3 = lst.find_all(class_='line-title fluid-line-title')

        zipped = list(zip(lst3, lst2))
        return zipped
