import services.waterstones as ws
import config


def get_services():
    return [ws.BooksOfTheMonthService(config.books_of_the_month_url),
            ws.ComingSoonService(),
            ws.ComingSoonService()]
