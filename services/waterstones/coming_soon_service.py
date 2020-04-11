from services import ServiceStrategy


class ComingSoonService(ServiceStrategy):
    def get_service_name(self):
        return "coming_soon_service"

    def get_data(self):
        pass
