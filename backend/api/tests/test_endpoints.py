from .test_setup import TestSetUp
from rest_framework import status
from ..models import Listing, FavoriteListing
from django.db.utils import IntegrityError


class AccountTests(TestSetUp):
    def test_can_create_account(self):
        """
        Ensure we can create a new account object. (valid data)
        """
        response = self.client.post(
            self.account_endpoint,
            self.user_data_valid,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        userObj = self.user_model.objects.get(
            email=self.user_data_valid['email'])
        self.assertEqual(self.user_model.objects.count(), 3)
        self.assertEqual(userObj.first_name, 'Testing')
        self.assertEqual(userObj.last_name, 'Endpoints')
        self.assertTrue(userObj.is_active)
        self.assertFalse(userObj.is_staff)
        self.assertFalse(userObj.is_superuser)
        self.assertEqual(userObj.get_full_name(),
                         'Testing Endpoints')

    def test_can_not_create_account(self):
        """
        Ensure we can not create a new account object (invalid data).
        """
        response = self.client.post(
            self.account_endpoint, self.user_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user_model.objects.count(), 2)

    def test_responses_endpoint(self):
        """
        Ensure we can only use the right method or permission.
        """
        # ---------- RIGHT METHOD ----------#
        # CREATE USER VIEW SHOULD ONLY TAKE "POST"
        response = self.client.get(self.account_endpoint)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # RETRIEVE USER INFORMATION VIEW SHOULD ONLY TAKE "GET"
        response = self.client.post(
            f'{self.account_endpoint}{self.authenticated_user["token"]}/', data={}, HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # AUTHENTICATION VIA TOKEN SHOULD ONLY ACCEPT "POST"
        response = self.client.get(self.auth_endpoint)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # FAVORITE CREATE SHOULD ONLY TAKE "POST"
        response = self.client.get(self.listing_favorite_endpoint,
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # FAVORITE DESTROY SHOULD ONLY TAKE "DELETE"
        response = self.client.get(f"{self.listing_favorite_endpoint}123/",
                                   HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # ---------- PERMISSIONS ----------#
        # RETRIEVE USER INFORMATION REQUIRES TO BE LOGGED IN
        response = self.client.get(
            f'{self.account_endpoint}{self.authenticated_user["token"]}/')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # LISTING GET **ALL** INFORMATION REQUIRES TO BE LOGGED IN
        response = self.client.get(self.listing_endpoint)
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # LISTING CREATE REQUIRES TO BE LOGGED IN
        response = self.client.post(self.listing_endpoint, data={})
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # FAVORITE CREATE VIEW REQUIRES TO BE LOGGED IN
        response = self.client.post(self.listing_favorite_endpoint, data={})
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        # FAVORITE DELETE VIEW REQUIRES TO BE LOGGED IN
        response = self.client.delete(
            f"{self.listing_favorite_endpoint}anystrpkwilldo/")
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_can_get_token(self):
        """
        Make sure we can authenticate users via a token (setup provides 2 user accounts)
        """
        # Logging in user 1
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

    def test_can_get_user(self):
        """
        Make sure we can get user information
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

    def test_can_create_listing(self):
        """
        Make sure we can create listings with (valid data)
        """
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
        self.assertEqual(response.data['creator'],
                         self.authenticated_user['user'])

    def test_can_get_listings(self):
        """
        MAKE SURE WE CAN GET **ALL** LISTINGS AND MAKE SURE DATA IS ACCURATE
        """
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

    def test_can_not_create_listing(self):
        """
        Make sure we can not create listing (invalid data)
        """
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_create_favorite(self):
        """
        Make sure we can create favorites
        """
        # based on loggedin user
        # listing needs to exists or 404
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

    def test_can_delete_favorite(self):
        # Created a post to delete!
        response = self.client.post(self.listing_favorite_endpoint, {
            "listingID": self.listing.id
        }, format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        id = response.data['id']
        # Make sure it was created!
        self.assertEqual(FavoriteListing.objects.count(), 2)
        # Attempts to delete it:
        # CASE: without logged in
        response = self.client.delete(
            f'{self.listing_favorite_endpoint}{id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # CASE: not beign the owner user
        response = self.client.delete(f'{self.listing_favorite_endpoint}{self.favorited_by_second_user.id}/',
                                      format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # FINALLY deleting with beign logged in / ownership
        response = self.client.delete(f'{self.listing_favorite_endpoint}{id}/',
                                      format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FavoriteListing.objects.count(), 1)
        # can not delete invalid listings
        response = self.client.delete(f'{self.listing_favorite_endpoint}12312312/',
                                      format='json', HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
