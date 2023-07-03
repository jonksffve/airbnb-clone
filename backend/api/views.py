from rest_framework.generics import (CreateAPIView,
                                     ListCreateAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
# from .permissions import IsOwnerOrStaff (deprecated, is done by QuerySets now)

from accounts.serializers import UserSerializer, TokenSerializer
from .serializers import (
    ListingSerializer,
    FavoriteCreateSerializer,
    FavoriteListSerializer,
    ReservationCreateSerializer,
    ReservationListSerializer)

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Listing, Category, FavoriteListing, ReservationListing

# Get the current User model
user_model = get_user_model()


class UserCreateView(CreateAPIView):
    """
    Creates a new user with the given data.
    @accepts: only POST method
    """
    queryset = user_model.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):
    """
    Returns valid credentials so user can log in.
    Also returns the authenticated user information for front-end usage.
    @accepts: [POST]
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': serializer.data
        })


class UserRetrieveView(RetrieveAPIView):
    """
    Retrieve a single user information with the provided Token authentication value.
    @permissions: user needs to be authenticated
    @accepts: [GET]
    """
    permission_classes = [IsAuthenticated]
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'


class ListingCreateListView(ListCreateAPIView):
    """
    Creates a new instance OR returns list of objects, depending on the method.
    @permissions: user needs to be authenticated
    @accepts: [GET, POST]
    @Raises 400, 404
    """
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def create(self, request, *args, **kwargs):
        # raises 400 if not given category in the body
        try:
            category_name = request.data['category']
        except:
            raise ParseError

        # raises 404 if category doesnt exists
        category_obj = get_object_or_404(
            Category, name=category_name)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, category_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, category_obj):
        serializer.save(creator=self.request.user, category=category_obj)


class FavoriteCreateListView(ListCreateAPIView):
    """
    View that will create/list favorite instances based on request.method
    @ permissions: user needs to be authenticated
    @ accepts: [GET, POST]
    """
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = None

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FavoriteListSerializer
        return FavoriteCreateSerializer

    def get_queryset(self):
        return FavoriteListing.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Make sure listingID is passed or 400
        try:
            listing_id = request.data['listingID']
        except:
            raise ParseError

        # Make sure listing instance exists
        listing = get_object_or_404(Listing, pk=listing_id)

        serializer = self.get_serializer(
            data={"listing": listing.id, "user": request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FavoriteDestroyView(DestroyAPIView):
    """
    Deletes a model instance of FavoriteListing
    @ permissions: user needs to be authenticated and be the owner of the object itself.
    #### (this is done by filtering querysets based in: current_user and listing)
    @ accepts: [DELETE]
    """
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = FavoriteListSerializer
    lookup_field = 'listing'

    def get_queryset(self):
        # We make sure to filter the data based on loggedin user, so he is the owner!
        return FavoriteListing.objects.filter(user=self.request.user)


class ListingRetrieveView(RetrieveAPIView):
    """
    Retrieves a single instance of a Listing model
    @ permissions: user needs to be authenticated
    @ accepts: [GET]
    """
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ReservationListCreateView(ListCreateAPIView):
    """
    View that will attempt to create a Reservation if POST
    OR get all reservations on a listing (if listingID provided) or return all user reservations (no params)
    @ permissions: user needs to be authenticated
    @ accepts: [GET, POST]
    """
    permission_classes = [IsAuthenticated]
    queryset = None

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            # Used for listing nested relationship information such as (user) and (listing)
            return ReservationListSerializer
        # Has validations on the date fields logic!
        return ReservationCreateSerializer

    def get_queryset(self):
        # IF we need reservations on a particular listing we first attempt to get that ID
        if 'listingID' in self.request.query_params:
            # We raise 404 is provided listing is not accurate for a particular listing
            listing = get_object_or_404(
                Listing, pk=self.request.query_params['listingID'])
            queryset = ReservationListing.objects.filter(
                listing=listing, end_date__gte=now())
        else:
            # IF we fail to get listingID we then return all of the authenticated user's reservations
            queryset = ReservationListing.objects.filter(
                user=self.request.user)

        return queryset

    def create(self, request, *args, **kwargs):
        # Try to get full data from front-end
        try:
            data = {
                "listing": request.data['listingID'],
                "user": request.user.id,
                "start_date": request.data['start_date'],
                "end_date": request.data['end_date'],
            }
        except:
            # [ref] https://www.django-rest-framework.org/api-guide/exceptions/#parseerror
            raise ParseError
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReservationDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = ReservationListSerializer

    def get_queryset(self):
        # We make sure to filter the data based on loggedin user, so he is the owner!
        return ReservationListing.objects.filter(user=self.request.user)
