from services import ServiceStrategy


class WaterstonesBaseService(ServiceStrategy):
    def get_service_family_name(self):
        return 'waterstones'
