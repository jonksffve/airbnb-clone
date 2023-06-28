from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ..models import Category


class TestSetUp(APITestCase):
    def setUp(self):
        self.account_endpoint = "/api/account/"
        self.auth_endpoint = "/api/auth/token_auth/"
        self.listing_endpoint = "/api/listing/"

        self.user_model = get_user_model()
        self.user_object = self.user_model.objects.create_user(
            email="normal@user.com", password="foo123", first_name="Test", last_name="Prueba")
        response = self.client.post(self.auth_endpoint, {
            'username': 'normal@user.com',
            'password': 'foo123'
        })

        self.cat = Category.objects.create(name='Castillo')

        self.authenticated_user = response.data

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
