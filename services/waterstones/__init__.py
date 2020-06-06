"""The Waterstones specific services."""
from .books_of_month_service import (  # noqa: F401
    BooksOfTheMonthScrapingService,
    BooksOfTheMonthService,
)
from .coming_soon_service import (  # noqa: F401
    ComingSoonScrapingService,
    ComingSoonService,
)
from .merging_service import MergingService  # noqa: F401
from .new_books_service import NewBooksScrapingService, NewBooksService  # noqa: F401
from .rating_service import RatingService  # noqa: F401
