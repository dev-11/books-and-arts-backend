import requests
import json


class RatingService:
    def __init__(self, api_key):
        """Goodreads ratings."""
        self._url = "https://www.goodreads.com/book/review_counts.json"
        self._api_key = api_key

    def get_ratings(self, isbns: []):
        isbn_str = ",".join(isbns)
        ratings = requests.get(f"{self._url}?isbns={isbn_str}&key={self._api_key}")
        return json.loads(ratings.text)
