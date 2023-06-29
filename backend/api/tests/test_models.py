from django.test import TransactionTestCase
from api.models import Listing, Category, FavoriteListing
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model


class ListingsTestCase(TransactionTestCase):
    def setUp(self):
        self.user_obj = get_user_model().objects.create_user(
            email="normal@user.com", password="foo", first_name="Test", last_name="Prueba")
        self.cat = Category.objects.create(name="Castillos")
        self.listing = Listing.objects.create(
            creator=self.user_obj,
            title='Castillo sano',
            description="Castillo en la punta del cerro, con vista al mar",
            price=26.50,
            guestCount=2,
            roomCount=2,
            bathroomCount=2,
            category=self.cat,
            location="USA")
        self.favorite = FavoriteListing.objects.create(
            listing=self.listing, user=self.user_obj)

    def test_listings_creation(self):
        """
        Testing restrictions on how you can (or not) create listings
        """
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(self.listing.title, 'Castillo sano')
        self.assertEqual(str(self.listing), 'Castillo sano')
        self.assertEqual(self.listing.price, 26.50)
        self.assertEqual(self.listing.category, self.cat)
        self.assertEqual(self.listing.creator, self.user_obj)

    def test_wrong_creation(self):
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
        self.assertEqual(self.favorite.user, self.user_obj)
        self.assertEqual(self.favorite.listing, self.listing)
        self.assertEqual(self.favorite.user.first_name, 'Test')
        self.assertEqual(str(self.favorite), 'Test Prueba favorites 1')
        # with nothing
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create()
        # with user
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(user=self.user_obj)
        # with listing
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(listing=self.listing)
        # duplicated
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(
                user=self.user_obj, listing=self.listing)
        self.assertEqual(FavoriteListing.objects.count(), 1)
