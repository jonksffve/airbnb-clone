from django.test import TransactionTestCase
from api.models import Listing, Category
from django.db.utils import IntegrityError


class ListingsTestCase(TransactionTestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Castillos")
        self.listing = Listing.objects.create(
            title='Castillo sano',
            description="Castillo en la punta del cerro, con vista al mar",
            price=26.50,
            guestCount=2,
            roomCount=2,
            bathroomCount=2,
            category=self.cat,
            location="USA")

    def test_listings_creation(self):
        """
        Testing restrictions on how you can (or not) create listings
        """
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(self.listing.title, 'Castillo sano')
        self.assertEqual(str(self.listing), 'Castillo sano')
        self.assertEqual(self.listing.price, 26.50)
        self.assertEqual(self.listing.category, self.cat)

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
