import services.waterstones as ws
import services.national_gallery as ng
import services.cache_service as cs
import repositories.s3_repository as s3r
import services.storage_service as ss
import config
import secrets


class ServiceFactory:
    def __init__(self):
        repo = s3r.S3Repository(config.data_bucket)
        storage = ss.StorageService(repo)
        self._cache = cs.CacheService(storage)
        try:
            key = secrets.good_reads_api_key
        except AttributeError:
            key = ''
        self._merging_service = ws.MergingService(ws.RatingService(key))

    def get_all_services(self):
        return [self.get_waterstones_books_of_the_month_service(),
                self.get_waterstones_coming_soon_service(),
                self.get_waterstones_new_books_service(),
                self.get_ng_current_exhibitions_service(),
                self.get_ng_coming_soon_service()]

    def get_ng_current_exhibitions_service(self):
        scraping_service = ng.CurrentExhibitionsScrapingService(config.exhibitions_urls)
        return ng.CurrentExhibitionsService(scraping_service, self._cache)

    def get_ng_coming_soon_service(self):
        scraping_service = ng.ComingSoonScrapingService(config.exhibitions_urls)
        return ng.ComingSoonService(scraping_service, self._cache)

    def get_waterstones_books_of_the_month_service(self):
        scraping_service = ws.BooksOfTheMonthScrapingService(config.books_of_the_month_url)
        return ws.BooksOfTheMonthService(scraping_service, self._cache, self._merging_service)

    def get_waterstones_coming_soon_service(self):
        scraper = ws.ComingSoonScrapingService(config.coming_soon_url)
        return ws.ComingSoonService(scraper, self._cache, self._merging_service)

    def get_waterstones_new_books_service(self):
        scraper = ws.NewBooksScrapingService(config.new_books_url)
        return ws.NewBooksService(scraper, self._cache, self._merging_service)


def get_enabled_services():
    return [service for service in ServiceFactory().get_all_services()
            if service.get_service_full_name() in config.enabled_services]
