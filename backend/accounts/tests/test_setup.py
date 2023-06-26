from django.test import TestCase
from django.contrib.auth import get_user_model


class TestSetUp(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user_object = self.user_model.objects.create_user(
            email="normal@user.com", password="foo", first_name="Test", last_name="Prueba")
        self.admin_object = self.user_model.objects.create_superuser(
            email="super@user.com", first_name="admin", last_name="admin", password="foo")

        return super().setUp()
