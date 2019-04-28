from django.test import TestCase

import ast

from rest_framework.test import APIRequestFactory

from .views import configuration_get
from .models import Configuration


class ConfigurationTest(TestCase):

    # Tests set up and tear down
    def setUp(self):
        configuration = Configuration.objects.create(maximum_radius=20000, minimum_radius=20,
                                                     time_listen_advertisement=3.0, minimum_reports_ban=10,
                                                     time_extend_audio=3600)
        configuration.save()

    def tearDown(self):
        Configuration.objects.all().delete()

    # Test cases
    def test_get_configuration(self):

        # Get configuration
        self.get_configuration(200)

    def get_configuration(self, code):

        factory = APIRequestFactory()
        request = factory.get('/configuration/', content_type='application/json')
        response = configuration_get(request)
        r = ast.literal_eval(response.getvalue().decode())

        self.assertTrue(response.status_code == code)
        self.assertTrue(r['maximum_radius'] == 20000)
        self.assertTrue(r['minimum_radius'] == 20)
        self.assertTrue(r['time_listen_advertisement'] == 3.0)
        self.assertTrue(r['minimum_reports_ban'] == 10)
        self.assertTrue(r['time_extend_audio'] == 3600)
