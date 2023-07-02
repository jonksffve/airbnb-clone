from .test_setup import TestSetUp
from rest_framework import status
from ..models import Listing, FavoriteListing, ReservationListing
from django.db.utils import IntegrityError
from django.utils.timezone import now, timedelta


class AccountTests(TestSetUp):
    def test_reservation_endpoint(self):
        """
        Basic testing to ensure the functionality of this endpoint
        @accepts: [GET, POST]
        """

        # User needs to be authenticated for both GET, POST methods
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now() + timedelta(9),
            "end_date": now() + timedelta(14),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.reservation_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # We're filtering the data based on listings:
        # Returns http400 if we don't attach "listingID" as query_params
        response = self.client.get(f'{self.reservation_endpoint}?listing=123',
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Returns http404 if listing does not exists
        response = self.client.get(f'{self.reservation_endpoint}?listingID=123',
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Succesfully create an object
        response = self.client.post(self.reservation_endpoint, {
            "listingID": self.listing.id,
            "start_date": now() + timedelta(9),
            "end_date": now() + timedelta(14),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['listing'], self.listing.id)
        self.assertEqual(response.data['user'], self.first_user_obj.id)
        self.assertEqual(ReservationListing.objects.count(), 2)
        newCreatedListingID = response.data['listing']

        # Testing GET method
        response = self.client.get(f'{self.reservation_endpoint}?listingID={newCreatedListingID}',
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validation no data
        response = self.client.post(self.reservation_endpoint, {
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Validation dates (past date)
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now() - timedelta(1),
            "end_date": now() + timedelta(6),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Validation dates (end date lower than start date)
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now(),
            "end_date": now() - timedelta(1),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # By default in our setup file, the current listing is reserved for a week from timezone.now() + 1 day
        # Validating that we can't reserved any day from now up to a week since tomorrow
        #
        # Validating case in between reservation
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now() + timedelta(2),
            "end_date": now() + timedelta(4),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Validating equal reservation
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now() + timedelta(1),
            "end_date": now() + timedelta(8),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Validating bigger (range) reservation
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now(),
            "end_date": now() + timedelta(10),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Validating just 1 day reserved in between a bigger reservation
        # Can create 1 day/night reservation
        # Creation:
        ReservationListing.objects.create(listing=self.listing, user=self.first_user_obj, start_date=now(
        ) + timedelta(15), end_date=now() + timedelta(15))
        # Validation:
        response = self.client.post(self.reservation_endpoint, {
            "listing": self.listing.id,
            "start_date": now() + timedelta(10),
            "end_date": now() + timedelta(20),
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ReservationListing.objects.count(), 3)

    def test_account_endpoint(self):
        """
        Tests defined to check the usage of the UserCreateView
        @accepts: [POST]
        """
        # Ensure we can create accounts (valid data)
        response = self.client.post(
            self.account_endpoint, self.user_data_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_model.objects.count(), 3)

        # Ensure we can not create a new account object (invalid data).
        response = self.client.post(
            self.account_endpoint, self.user_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user_model.objects.count(), 3)

    def test_account_retrieve_endpoint(self):
        """
        Make sure we can get user information to this endpoint
        @ needs to be authenticated
        @ accepts [GET]
        """
        response = self.client.get(
            f"{self.account_endpoint}{self.authenticated_user['token']}/", HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'],
                         self.authenticated_user['user']['first_name'])
        self.assertEqual(response.data['user']['last_name'],
                         self.authenticated_user['user']['last_name'])
        self.assertEqual(response.data['user']['email'],
                         self.authenticated_user['user']['email'])
        # Checking authentication requirement
        response = self.client.get(
            f"{self.account_endpoint}{self.authenticated_user['token']}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorization_endpoint(self):
        """
        Tests to validate getting the token given a valid id
        @accepts: [POST]
        """
        # Logging user 1
        response = self.client.post(self.auth_endpoint, {
                                    'username': 'normal@user.com',
                                    'password': 'foo123'
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'],
                         self.first_user_obj.first_name)
        self.assertEqual(response.data['user']['last_name'],
                         self.first_user_obj.last_name)
        self.assertEqual(response.data['user']['email'],
                         self.first_user_obj.email)
        # Logging in user 2
        response = self.client.post(self.auth_endpoint, {
                                    'username': 'normal2@user.com',
                                    'password': 'foo123'
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'],
                         self.second_user_obj.first_name)
        self.assertEqual(response.data['user']['last_name'],
                         self.second_user_obj.last_name)
        self.assertEqual(response.data['user']['email'],
                         self.second_user_obj.email)
        # Trying wrong user
        response = self.client.post(self.auth_endpoint, {
                                    'username': 'wrong@user.com',
                                    'password': 'thisiswrong'
                                    })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_endpoint(self):
        """
        Testing ListCreate endpoint
        Endpoint used for both create and list all objects
        @ permission: needs authentication
        @ accepts [GET, POST]
        @ Raises 400,404
        """
        # Creating listings (valid data)
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'title': 'I have title',
                                        'description': 'This is my description',
                                        'price': '25.50',
                                        'guestCount': '2',
                                        'roomCount': '3',
                                        'bathroomCount': '2',
                                        'category': 'Castillo',
                                        'location': 'USA'},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}'
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'I have title')
        self.assertEqual(Listing.objects.count(), 2)
        self.assertEqual(response.data['creator']['first_name'],
                         self.authenticated_user['user']['first_name'])

        # Testing LISTING data
        # Authenticate second user (which has a listing liked)
        auth_second_user = self.client.post(self.auth_endpoint, {
            'username': 'normal2@user.com',
            'password': "foo123"
        }).data
        response_second_user = self.client.get(
            self.listing_endpoint, HTTP_AUTHORIZATION=f'Token {auth_second_user["token"]}')
        self.assertEqual(response_second_user.status_code, status.HTTP_200_OK)
        # make sure favorited is TRUE for second user
        self.assertTrue(response_second_user.data[0]['is_liked'])
        response_first_user = self.client.get(
            self.listing_endpoint, HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        # make sure favorited is FALSE for 1st user
        self.assertFalse(response_first_user.data[0]['is_liked'])

        # Testing situations in which we can't create
        # With empty title
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'title': '',
                                        'description': 'This is my description',
                                        'price': '25.50',
                                        'guestCount': '2',
                                        'roomCount': '3',
                                        'bathroomCount': '2',
                                        'category': 'Castillo',
                                        'location': 'USA'},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # with no title
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'description': 'This is my description',
                                        'price': '25.50',
                                        'guestCount': '2',
                                        'roomCount': '3',
                                        'bathroomCount': '2',
                                        'category': 'Castillo',
                                        'location': 'USA'},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # with negative price?
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'title': '',
                                        'description': 'This is my description',
                                        'price': '-1',
                                        'guestCount': '2',
                                        'roomCount': '3',
                                        'bathroomCount': '2',
                                        'category': 'Castillo',
                                        'location': 'USA'},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # IF category can't be found
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'title': '',
                                        'description': '',
                                        'price': '0',
                                        'guestCount': '0',
                                        'roomCount': '0',
                                        'bathroomCount': '0',
                                        'category': 'Castillo1',
                                        'location': ''},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # With ALL fields wrong (except category which raises a dif status)
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'title': '',
                                        'description': '',
                                        'price': '0',
                                        'guestCount': '0',
                                        'roomCount': '0',
                                        'bathroomCount': '0',
                                        'category': 'Castillo',
                                        'location': ''},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # IF category is not defined
        response = self.client.post(self.listing_endpoint,
                                    data={
                                        'title': '',
                                        'description': '',
                                        'price': '0',
                                        'guestCount': '0',
                                        'roomCount': '0',
                                        'bathroomCount': '0',
                                        'location': ''},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}'
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Permission: needs to be logged in
        response = self.client.get(self.listing_endpoint)
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_listing_retrieve_endpoint(self):
        """
        Test retrieving information for a single instance of a listing model
        @ permission: needs to be authenticated
        @ accepts: [GET]
        """
        # needs to be authenticated
        response = self.client.get(
            f"{self.listing_endpoint}{self.listing.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # invalid id
        response = self.client.get(f"{self.listing_endpoint}12313/",
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # retrieves a single instance model
        response = self.client.get(f"{self.listing_endpoint}{self.listing.id}/",
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.listing.id)
        self.assertEqual(response.data['title'], self.listing.title)
        self.assertEqual(
            response.data['creator']['first_name'], self.listing.creator.first_name)

    def test_favorite_endpoint(self):
        """
        Test creation of user favoriting a particular listing
        @ permissions: user needs to be authenticated
        @ accepts: [POST]
        """
        # listing id needs to be in request body or 400
        response = self.client.post(self.listing_favorite_endpoint, {
            "listing": self.listing.id
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # listing needs to exists or 404
        response = self.client.post(self.listing_favorite_endpoint, {
            "listingID": "131451"
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # 201 all O.K.
        response = self.client.post(self.listing_favorite_endpoint, {
            "listingID": self.listing.id
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteListing.objects.count(), 2)

        # can't favorite 2 times same listing
        with self.assertRaises(IntegrityError):
            self.client.post(self.listing_favorite_endpoint, {
                "listingID": self.listing.id
            }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
            self.assertEqual(FavoriteListing.objects.count(), 2)

        # authentication
        response = self.client.post(self.listing_favorite_endpoint, {
            "listingID": self.listing.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_favorite_destroy_endpoint(self):
        """
        Testing to delete listing favorite status by user
        @ permission: ownership (done via filtering queryset)
        @ permission: needs to be authenticated
        @ accepts: [DELETE]
        """
        # Created a favorite to delete!
        response = self.client.post(self.listing_favorite_endpoint, {
            "listingID": self.listing.id
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(FavoriteListing.objects.count(), 2)
        # Attempts to delete it:

        # CASE: without logged in
        response = self.client.delete(
            f'{self.listing_favorite_endpoint}{self.listing.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Deleting with beign logged in / ownership
        response = self.client.delete(f'{self.listing_favorite_endpoint}{self.listing.id}/',
                                      format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FavoriteListing.objects.count(), 1)

        # CASE: not beign the owner user (will throw a 404 since we can't find it!)
        response = self.client.delete(f'{self.listing_favorite_endpoint}{self.favorited_by_second_user.listing.id}/',
                                      format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # can not delete invalid listings
        response = self.client.delete(f'{self.listing_favorite_endpoint}12312312/',
                                      format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
