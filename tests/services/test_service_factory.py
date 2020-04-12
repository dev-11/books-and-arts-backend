import unittest
from services import service_factory
import config


class ServiceFactoryTests(unittest.TestCase):
    def test_get_all_services_returns_every_service(self):
        all_services = service_factory.get_all_services()
        self.assertEqual(3, len(all_services))

    def test_get_enabled_services_return_only_enabled_services(self):
        enabled_services = service_factory.get_enabled_services()
        for service in enabled_services:
            self.assertIn(service.get_service_name(), config.enabled_services)
