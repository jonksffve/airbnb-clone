from .test_setup import TestSetUp
from api.models import Listing, FavoriteListing, ReservationListing, Category
from django.db.utils import IntegrityError
from django.utils.timezone import now, timedelta


class ListingsTestCase(TestSetUp):
    def test_category_model(self):
        """
        Test for creation of Category instances (this will be done by admins)
        """
        second_category = Category.objects.create(name="New One")
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(second_category.name, "New One")

        # creation duplicated
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="New One")

        # STR method
        self.assertEqual(str(second_category), second_category.name)

    def test_listing_model(self):
        """
        Testing restrictions on how you can (or not) create listings
        """
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(self.listing.title, 'This is for testing')
        self.assertEqual(str(self.listing), 'This is for testing')
        self.assertEqual(self.listing.price, 25.50)
        self.assertEqual(self.listing.category, self.category)
        self.assertEqual(self.listing.creator, self.first_user_obj)

        # STR method
        self.assertEqual(str(self.listing), self.listing.title)

        # Empty instance
        with self.assertRaises(IntegrityError):
            Listing.objects.create()

        # Creating object without creator
        with self.assertRaises(IntegrityError):
            Listing.objects.create(
                title='Hola',
                description="Has description",
                price=25.06,
                guestCount=2,
                roomCount=2,
                bathroomCount=1,
                location="USA",
                category=self.category
            )

        # Creating object without category
        with self.assertRaises(IntegrityError):
            Listing.objects.create(
                title='Hola',
                description="Has description",
                price=25.06,
                guestCount=2,
                roomCount=2,
                bathroomCount=1,
                location="USA",
                creator=self.first_user_obj
            )

    def test_favorite_listing_model(self):
        """
        Tests used in order to determine favorite model usage
        On setUp we already favorited "self.listing with self.second_user_object"
        @ constraint: user+listing both are a compound pk
        """
        self.assertEqual(FavoriteListing.objects.count(), 1)
        self.assertEqual(self.favorited_by_second_user.user,
                         self.second_user_obj)
        self.assertEqual(self.favorited_by_second_user.listing, self.listing)
        self.assertEqual(
            self.favorited_by_second_user.user.first_name, 'Test 2')
        self.assertEqual(str(self.favorited_by_second_user),
                         'Test 2 Prueba 2 favorites This is for testing')
        # with nothing
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create()

        # with just user
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(user=self.first_user_obj)

        # with just listing
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(listing=self.listing)

        # constraint unique user and unique listing
        with self.assertRaises(IntegrityError):
            FavoriteListing.objects.create(
                user=self.second_user_obj, listing=self.listing)
        self.assertEqual(FavoriteListing.objects.count(), 1)

        # STR method
        self.assertEqual(str(self.favorited_by_second_user),
                         f"{self.second_user_obj.get_full_name()} favorites {self.listing.title}")

    def test_reservation_listing_model(self):
        # creation valid data
        reservation = ReservationListing.objects.create(
            listing=self.listing, user=self.first_user_obj, start_date=now(), end_date=(now() + timedelta(2)))
        self.assertEqual(ReservationListing.objects.count(), 2)
        self.assertEqual(reservation.listing, self.listing)
        self.assertEqual(reservation.user, self.first_user_obj)

        # creation no data
        with self.assertRaises(IntegrityError):
            ReservationListing.objects.create()

        # creation no listing
        with self.assertRaises(IntegrityError):
            ReservationListing.objects.create(
                user=self.first_user_obj, start_date=now(), end_date=(now() + timedelta(2)))

        # creation no user
        with self.assertRaises(IntegrityError):
            ReservationListing.objects.create(
                listing=self.listing, start_date=now(), end_date=(now() + timedelta(2)))

        # creation without start date
        with self.assertRaises(IntegrityError):
            ReservationListing.objects.create(
                listing=self.listing, user=self.first_user_obj, end_date=(now() + timedelta(2)))

        # creation without ending date
        with self.assertRaises(IntegrityError):
            ReservationListing.objects.create(
                listing=self.listing, user=self.first_user_obj, start_date=now())

        # creation with no dates
        with self.assertRaises(IntegrityError):
            ReservationListing.objects.create(
                listing=self.listing, user=self.first_user_obj)

        # STR method
        self.assertEqual(str(
            reservation), f"{self.first_user_obj.get_full_name()} reservated: {self.listing.title}")
