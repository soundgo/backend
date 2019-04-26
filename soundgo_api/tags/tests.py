from django.test import TestCase
import requests

# Create your tests here.


class TagTest(TestCase):

    def get_host(self):
        #return "http://127.0.0.1:8000"
        return "https://soundgo-api-v3.herokuapp.com"

    # Test cases
    def test_get_tag(self):

        # Get configuration
        self.get_tag(200)

    def get_tag(self, code):

        headers = {'content-type': 'application/json'}

        r = requests.get(self.get_host() + '/tags/', headers=headers)

        self.assertTrue(r.status_code == code)
