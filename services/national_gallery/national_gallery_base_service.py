from services import ServiceStrategy


class NationalGalleryBaseService(ServiceStrategy):
    def get_service_family_name(self):
        return 'national_gallery'
