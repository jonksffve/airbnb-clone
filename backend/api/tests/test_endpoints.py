from .test_setup import TestSetUp
from rest_framework import status


class AccountTests(TestSetUp):
    def test_can_create_account(self):
        """
        Ensure we can create a new account object. (valid data)
        """
        response = self.client.post(
            self.endpoint, self.user_data_valid, format='json')
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
            self.endpoint, self.user_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user_model.objects.count(), 1)

    def test_methods_endpoint(self):
        """
        Ensure we can only use the right method.
        """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_get_token(self):
        """
        Ensure we can create and get a token user
        """
        response = self.client.post(self.auth_endpoint, {
                                    'username': 'normal@user.com',
                                    'password': 'foo123'
                                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'],
                         self.user_object.first_name)
        self.assertEqual(response.data['last_name'],
                         self.user_object.last_name)
        self.assertEqual(response.data['email'],
                         self.user_object.email)

    def test_can_get_user(self):
        """
        Ensure we can get user information
        """
        response = self.client.get(
            f"{self.endpoint}{self.authenticated_user['token']}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'],
                         self.user_object.first_name)
        self.assertEqual(response.data['user']['last_name'],
                         self.user_object.last_name)
        self.assertEqual(response.data['user']['email'],
                         self.user_object.email)
