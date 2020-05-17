from .rating_service import RatingService


class MergingService:
    def __init__(self, rating_service: RatingService):
        """Service to merge ratings and books"""
        self._rating_service = rating_service

    def merge(self, book_sections, isbns):
        ratings = self._rating_service.get_ratings(isbns)

        for bs in book_sections:
            for book in bs['books']:
                r = list(filter(lambda x: x['isbn13'] == book['isbn'], ratings['books']))
                book['rating'] = r[0] if len(r) >  0 else {}
        return book_sections
