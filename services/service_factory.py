import services.waterstones as ws
import services.national_gallery as ng
import config


def get_all_services():
    return [ws.BooksOfTheMonthService(config.books_of_the_month_url),
            ws.ComingSoonService(config.coming_soon_url),
            ws.NewBooksService(config.new_books_url),
            ng.CurrentExhibitionsService(config.exhibitions_urls)]


def get_enabled_services():
    return [service for service in get_all_services()
            if service.get_service_name() in config.enabled_services]
