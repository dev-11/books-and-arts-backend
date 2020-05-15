import requests
import json

class RatingService:
    def __init__(self, api_key):
        self._url = 'https://www.goodreads.com/book/review_counts.json'
        self._api_key= api_key

    def get_ratings(self, isbns: []):
        ratings = requests.get(f'{self._url}?isbns={isbns}&key={self._api_key}')
        return json.loads(ratings.text)
