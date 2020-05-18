import unittest
from services.waterstones import BooksOfTheMonthService
from datetime import datetime as dt
from datetime import timedelta as td


class TestBooksOfTheMonthService(unittest.TestCase):
    def test_get_expiry_date_returns_last_second_of_prev_month(self):
        botms = BooksOfTheMonthService(None, None, None)
        expiry_date = botms.get_expiry_date()
        now = dt.now()
        self.assertEqual(dt(now.year, now.month, 1, 0, 0, 0),
                         expiry_date + td(seconds=1))

    def test_get_service_family_name_returns_correct_value(self):
        botms = BooksOfTheMonthService(None, None, None)
        service_family_name = botms.get_service_family_name()
        self.assertEqual('waterstones', service_family_name)

    def test_get_service_name_returns_correct_value(self):
        botms = BooksOfTheMonthService(None, None, None)
        service_name = botms.get_service_name()
        self.assertEqual('books_of_the_month', service_name)

    def test_get_service_type_returns_correct_value(self):
        botms = BooksOfTheMonthService(None, None, None)
        service_type = botms.get_service_type()
        self.assertEqual('books', service_type)

    def test_get_service_full_name_returns_correct_value(self):
        botms = BooksOfTheMonthService(None, None, None)
        full_name = botms.get_service_full_name()
        self.assertEqual('waterstones.books_of_the_month', full_name)
