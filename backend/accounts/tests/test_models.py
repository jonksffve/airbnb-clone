from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com", password="foo", first_name="Test", last_name="Prueba")
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Prueba")
        self.assertEqual(user.get_full_name(), "Test Prueba")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="normal@user.com", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", first_name="admin", last_name="admin", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertEqual(admin_user.first_name, "admin")
        self.assertEqual(admin_user.last_name, "admin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)
        with self.assertRaises(IntegrityError):
            User.objects.create_superuser(
                email="super@user.com", password="foo")
