'''
from django.test import TestCase

class TestHomeUrl(TestCase):
    def test_home_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
'''
