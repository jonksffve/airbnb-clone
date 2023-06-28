from .test_setup import TestSetUp
from rest_framework import status
from ..models import Listing


class AccountTests(TestSetUp):
    def test_can_create_account(self):
        """
        Ensure we can create a new account object. (valid data)
        """
        response = self.client.post(
            self.account_endpoint, self.user_data_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        userObj = self.user_model.objects.get(
            email=self.user_data_valid['email'])
        self.assertEqual(self.user_model.objects.count(), 2)
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
        self.assertEqual(self.user_model.objects.count(), 1)

    def test_responses_endpoint(self):
        """
        Ensure we can only use the right method or permission.
        """
        # ---------- RIGHT METHOD ----------#
        # CREATE USER VIEW SHOULD ONLY TAKE "POST"
        response = self.client.get(self.account_endpoint)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        # CREATE LISTING VIEW SHOULD ONLY TAKE "POST"
        response = self.client.get(
            self.listing_endpoint, HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
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

        # ---------- PERMISSIONS ----------#
        response = self.client.post(self.listing_endpoint, data={})
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(
            f'{self.account_endpoint}{self.authenticated_user["token"]}/')
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_can_get_token(self):
        """
        Ensure we can create and get a token user
        """
        response = self.client.post(self.auth_endpoint, {
                                    'username': 'normal@user.com',
                                    'password': 'foo123'
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'],
                         self.user_object.first_name)
        self.assertEqual(response.data['user']['last_name'],
                         self.user_object.last_name)
        self.assertEqual(response.data['user']['email'],
                         self.user_object.email)

    def test_can_get_user(self):
        """
        Ensure we can get user information
        """
        response = self.client.get(
            f"{self.account_endpoint}{self.authenticated_user['token']}/", HTTP_AUTHORIZATION=f'Token {self.authenticated_user["token"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'],
                         self.user_object.first_name)
        self.assertEqual(response.data['user']['last_name'],
                         self.user_object.last_name)
        self.assertEqual(response.data['user']['email'],
                         self.user_object.email)

    def test_can_create_listing(self):
        """
        Ensure we can create Listing
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
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(response.data['creator'],
                         self.authenticated_user['user'])

    def test_can_not_create_listing(self):
        """
        Ensure we can not create Listing
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
