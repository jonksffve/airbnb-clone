from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        self.endpoint = "/api/account/"

        self.user_data_valid = {
            'first_name': 'Testing',
            'last_name': 'Endpoints',
            'email': 'testing@site.com',
            'password': '1234567',
        }

        self.user_data_invalid = {
            'first_name': '',
            'last_name': 'Endpoints',
            'email': "testing@site.com",
            'password': '1234'
        }

        return super().setUp()
