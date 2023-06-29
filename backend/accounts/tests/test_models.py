from django.db import IntegrityError
from .test_setup import TestSetUp


class UsersManagersTests(TestSetUp):
    def test_create_user(self):
        """
        Testing normal account User model
        """
        self.assertEqual(self.user_object.email, "normal@user.com")
        self.assertEqual(self.user_object.first_name, "Test")
        self.assertEqual(self.user_object.last_name, "Prueba")
        self.assertEqual(self.user_object.get_full_name(), "Test Prueba")
        self.assertTrue(self.user_object.is_active)
        self.assertFalse(self.user_object.is_staff)
        self.assertFalse(self.user_object.is_superuser)
        self.assertEqual(self.user_model.objects.count(), 2)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(self.user_object.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            self.user_model.objects.create_user()
        with self.assertRaises(TypeError):
            self.user_model.objects.create_user(email="")
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(email="", password="foo")
        with self.assertRaises(IntegrityError):
            self.user_model.objects.create_user(
                email="normal@user.com", password="foo")

    def test_create_superuser(self):
        """
        Testing superuser account User model
        """
        self.assertEqual(self.admin_object.email, "super@user.com")
        self.assertEqual(self.admin_object.first_name, "admin")
        self.assertEqual(self.admin_object.last_name, "admin")
        self.assertTrue(self.admin_object.is_active)
        self.assertTrue(self.admin_object.is_staff)
        self.assertTrue(self.admin_object.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(self.admin_object.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)
        with self.assertRaises(IntegrityError):
            self.user_model.objects.create_superuser(
                email="super@user.com", password="foo")
