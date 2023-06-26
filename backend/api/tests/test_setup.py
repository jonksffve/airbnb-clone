from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class TestSetUp(APITestCase):
    def setUp(self):
        self.endpoint = "/api/account/"
        self.auth_endpoint = "/api/account/auth/"

        self.user_model = get_user_model()
        self.user_object = self.user_model.objects.create_user(
            email="normal@user.com", password="foo123", first_name="Test", last_name="Prueba")

        self.user_data_valid = {
            'first_name': 'Testing',
            'last_name': 'Endpoints',
            'email': 'testing@site.com',
            'password': '1234567',
        }

        self.user_data_invalid = {
            'first_name': '',
            'last_name': 'Endpoints',
            'email': "normal@user.com",
            'password': '1234'
        }

        return super().setUp()