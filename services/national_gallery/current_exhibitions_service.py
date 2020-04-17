from .national_gallery_base_service import InnerService


class CurrentExhibitionsService(InnerService):
    def __init__(self, url):
        self._url = url

    def get_data(self):
        zipped = self.get_data()

        return self.get_exhibition_details(zipped[0])
