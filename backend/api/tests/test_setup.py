from rest_framework.test import APITransactionTestCase
from django.contrib.auth import get_user_model
from ..models import Category, Listing, FavoriteListing, ReservationListing
from django.utils.timezone import now, timedelta


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
        self.reservation_endpoint = "/api/reservation/"

        ####
        # BASIC INSTANCES CONFIG SETUP
        ####
        # USER MODEL
        self.user_model = get_user_model()

        # 5 DIFFERENT USERS
        self.first_user_obj = self.user_model.objects.create_user(
            email="normal@user.com",
            password="foo123",
            first_name="Test",
            last_name="Prueba",
        )
        self.second_user_obj = self.user_model.objects.create_user(
            email="normal2@user.com",
            password="foo123",
            first_name="Test 2",
            last_name="Prueba 2",
        )
        self.third_user_obj = self.user_model.objects.create_user(
            email="normal3@user.com",
            password="foo123",
            first_name="Test 3",
            last_name="Prueba 3",
        )
        self.forth_user_obj = self.user_model.objects.create_user(
            email="normal4@user.com",
            password="foo123",
            first_name="Test 4",
            last_name="Prueba 4",
        )
        self.fifth_user_obj = self.user_model.objects.create_user(
            email="normal5@user.com",
            password="foo123",
            first_name="Test 4",
            last_name="Prueba 4",
        )

        # 1 CATEGORY TO WORK WITH
        self.category = Category.objects.create(name="Castillo")

        # 3 LISTINGS TO WORK WITH
        self.listing = Listing.objects.create(
            creator=self.first_user_obj,
            title="This is for testing",
            description="Testing",
            price=25.50,
            guestCount=2,
            roomCount=3,
            bathroomCount=2,
            category=self.category,
            location="US",
        )
        self.listing_two = Listing.objects.create(
            creator=self.second_user_obj,
            title="This is for testing 2",
            description="Testing 2",
            price=25.50,
            guestCount=2,
            roomCount=3,
            bathroomCount=2,
            category=self.category,
            location="CA",
        )
        self.listing_three = Listing.objects.create(
            creator=self.third_user_obj,
            title="This is for testing",
            description="Testing",
            price=25.50,
            guestCount=2,
            roomCount=3,
            bathroomCount=2,
            category=self.category,
            location="GB",
        )

        # 2 FAVORITE LISTING TO WORK WITH
        self.favorited_by_first_user = FavoriteListing.objects.create(
            listing=self.listing_two, user=self.first_user_obj
        )

        self.favorited_by_second_user = FavoriteListing.objects.create(
            listing=self.listing, user=self.second_user_obj
        )

        # 3 RESERVATIONS TO WORK WITH AND CHECK DATE RESTRICTIONS! UP TO A WEEK SINCE TOMORROW!
        self.reservation = ReservationListing.objects.create(
            listing=self.listing,
            user=self.second_user_obj,
            start_date=(now() + timedelta(1)),
            end_date=(now() + timedelta(8)),
        )
        self.reservation_two = ReservationListing.objects.create(
            listing=self.listing,
            user=self.third_user_obj,
            start_date=(now() + timedelta(1)),
            end_date=(now() + timedelta(8)),
        )
        self.reservation_three = ReservationListing.objects.create(
            listing=self.listing,
            user=self.forth_user_obj,
            start_date=(now() + timedelta(1)),
            end_date=(now() + timedelta(8)),
        )

        # 2 Authenticated users to check permissions
        self.authenticated_user = self.client.post(
            self.auth_endpoint, {"username": "normal@user.com", "password": "foo123"}
        ).data
        self.authenticated_second_user = self.client.post(
            self.auth_endpoint, {"username": "normal2@user.com", "password": "foo123"}
        ).data

        # DUMMY_DATA TO USE
        self.user_data_valid = {
            "first_name": "Testing",
            "last_name": "Endpoints",
            "email": "testing@site.com",
            "password": "1234567",
        }

        self.user_data_invalid = {
            "first_name": "",
            "last_name": "Endpoints",
            "email": "normal@user.com",
            "password": "1234",
        }

        return super().setUp()
