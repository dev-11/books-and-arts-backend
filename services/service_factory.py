import services.waterstones as ws
import services.national_gallery as ng
import services.cache_service as cs
import repositories.s3_repository as s3r
import services.storage_service as ss
import config


def get_all_services():
    repo = s3r.S3Repository(config.data_bucket)
    storage = ss.StorageService(repo)
    return [ws.BooksOfTheMonthService(config.books_of_the_month_url,
                                      cs.CacheService(storage)),
            # ws.ComingSoonService(config.coming_soon_url),
            # ws.NewBooksService(config.new_books_url),
            ng.CurrentExhibitionsService(config.exhibitions_urls),
            ng.ComingSoonService(config.exhibitions_urls)]


def get_enabled_services():
    return [service for service in get_all_services()
            if service.get_service_full_name() in config.enabled_services]
