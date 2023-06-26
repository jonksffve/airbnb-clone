from .test_setup import TestSetUp
from rest_framework import status
from accounts.models import User


class AccountTests(TestSetUp):
    def test_can_create_account(self):
        """
        Ensure we can create a new account object. (valid data)
        """
        response = self.client.post(
            self.endpoint, self.user_data_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, 'Testing')
        self.assertEqual(User.objects.get().last_name, 'Endpoints')
        self.assertTrue(User.objects.get().is_active)
        self.assertFalse(User.objects.get().is_staff)
        self.assertFalse(User.objects.get().is_superuser)
        self.assertEqual(User.objects.get().get_full_name(),
                         'Testing Endpoints')

    def test_can_not_create_account(self):
        """
        Ensure we can not create a new account object (invalid data).
        """
        self.client.post(self.endpoint, self.user_data_valid, format='json')
        response = self.client.post(
            self.endpoint, self.user_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, 'Testing')
        self.assertEqual(User.objects.get().get_full_name(),
                         'Testing Endpoints')
