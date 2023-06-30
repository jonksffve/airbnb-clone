from rest_framework.test import APITransactionTestCase
from django.contrib.auth import get_user_model
from ..models import Category, Listing, FavoriteListing


class TestSetUp(APITransactionTestCase):
    """
    Base setup case for all "API" tests (models and endpoints)
    """

    def setUp(self):
        ####
        # BASIC ENDPOINT CONFIG SETUP
        ####
        self.account_endpoint = "/api/account/"
        self.auth_endpoint = "/api/auth/token_auth/"
        self.listing_endpoint = "/api/listing/"
        self.listing_favorite_endpoint = "/api/listing/favorite/"

        ####
        # BASIC INSTANCES CONFIG SETUP
        ####
        # USER MODEL
        self.user_model = get_user_model()

        # 2 DIFFERENT USERS
        self.first_user_obj = self.user_model.objects.create_user(
            email="normal@user.com", password="foo123", first_name="Test", last_name="Prueba")
        self.second_user_obj = self.user_model.objects.create_user(
            email="normal2@user.com", password="foo123", first_name="Test 2", last_name="Prueba 2")

        # 1 CATEGORY TO WORK WITH
        self.category = Category.objects.create(name='Castillo')

        # 1 LISTING TO WORK WITH
        self.listing = Listing.objects.create(creator=self.first_user_obj,
                                              title="This is for testing",
                                              description="Testing",
                                              price=25.50,
                                              guestCount=2,
                                              roomCount=3,
                                              bathroomCount=2,
                                              category=self.category,
                                              location='US')

        # 1 FAVORITE LISTING TO WORK WITH
        self.favorited_by_second_user = FavoriteListing.objects.create(
            listing=self.listing, user=self.second_user_obj)

        # 1 Authenticated user to check permissions
        self.authenticated_user = self.client.post(self.auth_endpoint, {
            'username': 'normal@user.com',
            'password': 'foo123'
        }).data

        # DUMMY_DATA TO USE
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
