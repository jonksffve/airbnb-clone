from .test_setup import TestSetUp
from api.models import Listing, Category, FavoriteListing
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


class ListingsTestCase(TestSetUp):
    def test_listings_creation(self):
        """
        Testing restrictions on how you can (or not) create listings
        """
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(self.listing.title, 'This is for testing')
        self.assertEqual(str(self.listing), 'This is for testing')
        self.assertEqual(self.listing.price, 25.50)
        self.assertEqual(self.listing.category, self.category)
        self.assertEqual(self.listing.creator, self.first_user_obj)

    def test_wrong_creation(self):
        """
        Testing data validation on create
        """
        # Empty instance
        with self.assertRaises(IntegrityError):
            Listing.objects.create()

        # Creating object with empty title
        with self.assertRaises(IntegrityError):
            Listing.objects.create(
                title="",
                description="Has description",
                price=25.06,
                guestCount=2,
                roomCount=2,
                bathroomCount=1,
                location="USA")

        # Creating object without title
        with self.assertRaises(IntegrityError):
            Listing.objects.create(
                description="Has description",
                price=25.06,
                guestCount=2,
                roomCount=2,
                bathroomCount=1,
                location="USA")

        # Creating object without creator
        with self.assertRaises(IntegrityError):
            Listing.objects.create(
                title='Hola',
                description="Has description",
                price=25.06,
                guestCount=2,
                roomCount=2,
                bathroomCount=1,
                location="USA")

    def test_favorite_creation(self):
        """
        Tests used in order to determine favorite model usage
        """
        self.assertEqual(FavoriteListing.objects.count(), 1)
        self.assertEqual(self.favorited_by_second_user.user,
                         self.second_user_obj)
        self.assertEqual(self.favorited_by_second_user.listing, self.listing)
        self.assertEqual(self.favorited_by_second_user.user.first_name, 'Test')
        self.assertEqual(str(self.favorited_by_second_user),
                         'Test Prueba favorites This is for testing')
        # with nothing
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create()
        # with just "user"
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(user=self.first_user_obj)
        # with just "listing"
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(listing=self.listing)
        # duplicated
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(
                user=self.second_user_obj, listing=self.listing)
        self.assertEqual(FavoriteListing.objects.count(), 1)
