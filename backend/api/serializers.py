from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from .models import Listing, Category, FavoriteListing, ReservationListing
from accounts.serializers import UserSerializer
from django.utils.timezone import now


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ListingSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    is_liked = SerializerMethodField(read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'image', 'price', 'guestCount',
                  'roomCount', 'bathroomCount', 'category', 'location', 'creator', 'is_liked']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        qs = obj.favorites.filter(user=user)
        if qs.exists():
            return True
        return False


class FavoriteCreateSerializer(ModelSerializer):
    class Meta:
        model = FavoriteListing
        fields = ['listing', 'user']


class FavoriteListSerializer(ModelSerializer):
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = FavoriteListing
        fields = ['id', 'listing', 'user']


class ReservationCreateSerializer(ModelSerializer):
    class Meta:
        model = ReservationListing
        fields = ['listing', 'user', 'start_date', 'end_date']

    def validate(self, data):
        """
        Object field validation, checks over different cases
        Will raise ValidationError
        By default this exception results in a **response** with the HTTP status code "400 Bad Request".
        @[ref] https://www.django-rest-framework.org/api-guide/exceptions/#validationerror
        """
        # Start date can't be greater than ending date
        if data['start_date'].date() > data['end_date'].date():
            raise ValidationError(
                {'end_date': 'End of reservation can not happen before initial date.'})

        # Can't book if already reserved validation
        # Making sure we shrink the valid query: Active reservations on current listing
        qs = ReservationListing.objects.filter(
            listing=data['listing'], end_date__gte=now())

        # userStart <= EndingReserved AND userEnding >= StartReserved
        # @[ref] https://stackoverflow.com/questions/71291099/python-django-filter-avoid-overlapping-between-range-dates
        if qs.filter(start_date__lte=data['end_date'].date(), end_date__gte=data['start_date'].date()).exists():
            raise ValidationError(
                {'wrong_booking': 'Reservation can not be made for this period. Listing already reserved.'})

        # ALL O.K.
        return data

    def validate_start_date(self, value):
        """
        Validates that start date is gte that now()
        Both just the date (without hours:minutes:seconds:ms)
        """
        if value.date() < now().date():
            raise ValidationError(
                {'start_date': 'Reservation can not be made for past dates.'})

        return value


class ReservationListSerializer(ModelSerializer):
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ReservationListing
        fields = ['id', 'listing', 'user', 'start_date', 'end_date']
