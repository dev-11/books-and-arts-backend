from services.waterstones import BooksOfTheMonthService
import config


def get_services():
    return [BooksOfTheMonthService(config.books_of_the_month_url)]
