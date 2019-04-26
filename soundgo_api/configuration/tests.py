from django.test import TestCase
import requests

# Create your tests here.


class ConfigurationTest(TestCase):

    def get_host(self):
        #return "http://127.0.0.1:8000"
        return "https://soundgo-api-v3.herokuapp.com"

    # Test cases
    def test_get_configuration(self):

        # Get configuration
        self.get_configuration(200)

    def get_configuration(self, code):

        headers = {'content-type': 'application/json'}

        r = requests.get(self.get_host() + '/configuration/', headers=headers)

        self.assertTrue(r.status_code == code)
        self.assertTrue(r.json()['maximum_radius'] == 2000)
        self.assertTrue(r.json()['minimum_radius'] == 20)
        self.assertTrue(r.json()['time_listen_advertisement'] == 3.0)
        self.assertTrue(r.json()['minimum_reports_ban'] == 10)
        self.assertTrue(r.json()['time_extend_audio'] == 3600)
