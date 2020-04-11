from services import ServiceStrategy


class NewBooksService(ServiceStrategy):
    def get_service_name(self):
        return "new_books_service"

    def get_data(self):
        pass

