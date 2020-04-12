import services.waterstones as ws
import config


def get_all_services():
    return [ws.BooksOfTheMonthService(config.books_of_the_month_url),
            ws.ComingSoonService(),
            ws.ComingSoonService()]


def get_required_services():
    return [service for service in get_all_services()
            if service.get_service_name() in config.services]
