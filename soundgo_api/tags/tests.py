from django.test import TestCase

from rest_framework.test import APIRequestFactory

import ast

from .models import Tag
from .views import get_all_tags


class TagTest(TestCase):

    # Tests set up and tear down
    def setUp(self):

        tag1 = Tag.objects.create(name='Exam')
        tag1.save()

        tag2 = Tag.objects.create(name='Party')
        tag2.save()

    def tearDown(self):
        Tag.objects.all().delete()

    # Test cases
    def test_get_tags(self):

        self.get_tags(200)

    # Auxiliary methods
    def get_tags(self, code):

        factory = APIRequestFactory()

        request = factory.get('/tags/', content_type='application/json')

        response = get_all_tags(request)
        response_value = ast.literal_eval(response.getvalue().decode())

        self.assertTrue(response.status_code == code)
        self.assertTrue(len(response_value) == 2)
