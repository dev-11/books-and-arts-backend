"""The Waterstones specific services."""
from .books_of_month_service import (BooksOfTheMonthScrapingService,
                                     BooksOfTheMonthService)
from .coming_soon_service import ComingSoonScrapingService, ComingSoonService
from .merging_service import MergingService
from .new_books_service import NewBooksScrapingService, NewBooksService
from .rating_service import RatingService
