import unittest

import config
from services import service_factory as sf


class ServiceFactoryTests(unittest.TestCase):
    def test_get_all_services_returns_every_service(self):
        all_services = sf.ServiceFactory().get_all_services()
        self.assertEqual(5, len(all_services))

    def test_get_enabled_services_returns_only_enabled_services(self):
        enabled_services = sf.get_enabled_services()
        for service in enabled_services:
            self.assertIn(service.get_service_full_name(), config.enabled_services)
