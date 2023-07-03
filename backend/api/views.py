from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
)
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
    ReservationListSerializer,
)

from .models import Listing, Category, FavoriteListing, ReservationListing

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Get the current User model
user_model = get_user_model()


class UserCreateView(CreateAPIView):
    """
    Function used to create new accounts

    Accepts:
        [POST] method

    Returns:
        201 - Object created
        400 - Bad data that failed serializer validation
    """

    queryset = user_model.objects.all()
    serializer_class = UserSerializer


class UserRetrieveView(RetrieveAPIView):
    """
    Function used to retrieve information of the request.user - User model

    Permissions:
        User needs to be authenticated

    Accepts:
        [GET] method

    Returns:
        200 - If user was found
        401 - Unauthorized
        404 - If user not found
    """

    permission_classes = [IsAuthenticated]
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = "key"


class CustomAuthToken(ObtainAuthToken):
    """
    Gets or creates authentication token if valid user credentials (username, password) are provided
    Returns the authenticated user information

    Accepts:
        [POST] method

    Returns:
        200 - User with valid credentials
        400 - User with bad credentials
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user, context={"request": request})
        return Response({"token": token.key, "user": serializer.data})


class FavoriteCreateListView(ListCreateAPIView):
    """
    View that will create OR list favorite instances based on "request.method"

    Permissions:
        User needs to be authenticated

    Accepts:
        [GET, POST] methods

    Returns:
        200 - Return list of instance(s)
        201 - Created favorited
        400 - Invalidad data in validation or did not pass listingID
        401 - Unathorized
        404 - Listing object not found
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
            listing_id = request.data["listingID"]
        except:
            raise ParseError

        # Make sure listing instance exists
        listing = get_object_or_404(Listing, pk=listing_id)

        serializer = self.get_serializer(
            data={"listing": listing.id, "user": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class FavoriteDestroyView(DestroyAPIView):
    """
    Deletes an instance of FavoriteListing if given right information

    Permissions:
        User needs to be authenticated.

    Accepts:
        [DELETE] method

    Returns:
        204 - Instance deleted
        401 - Unathorized
        404 - Object not found
    """

    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = FavoriteListSerializer
    lookup_field = "listing"

    def get_queryset(self):
        # We make sure to filter the data based on loggedin user, so he is the owner!
        return FavoriteListing.objects.filter(user=self.request.user)


class ListingCreateListView(ListCreateAPIView):
    """
    Creates a new instance OR returns list of objects, depending on the method.

    Permissions:
        User needs to be authenticated

    Accepts:
        [GET, POST] methods

    Returns:
        200 - When everything went good and returns list
            - Either returns (via query_params):
                - Listings owned by request.user (Properties)
                - All listings
        201 - On succesful creation
        400 - Something went wrong validating data for creation
        401 - Unauthorized
        404 - Whatever you try to list was not found or category not found
    """

    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = ListingSerializer

    def get_queryset(self):
        if "user_only" in self.request.query_params:
            return Listing.objects.filter(creator=self.request.user)
        return Listing.objects.all()

    def create(self, request, *args, **kwargs):
        # raises 400 if not given category in the body
        try:
            category_name = request.data["category"]
        except:
            raise ParseError

        # raises 404 if category doesnt exist
        category_obj = get_object_or_404(Category, name=category_name)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, category_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, category_obj):
        serializer.save(creator=self.request.user, category=category_obj)


class ListingRetrieveDestroyView(RetrieveDestroyAPIView):
    """
    Retrieves a single instance of a Listing model OR destroys it depending on the method

    Permissions:
        User needs to be authenticated

    Accepts:
        [GET, DESTROY] methods

    Returns:
        200 - On listing items
        204 - On deletion if succesful
        401 - Unauthorized
        404 - Object not found to be deleted
    """

    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = ListingSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return Listing.objects.all()
        # This way we make sure request.user is the owner before deleting!
        return Listing.objects.filter(creator=self.request.user)


class ReservationListCreateView(ListCreateAPIView):
    """
    View that will attempt to create a Reservation if POST
    OR get all reservations on a listing (if listingID provided) or return all user reservations (no params)

    Permissions:
        User needs to be authenticated

    Accepts:
        [GET, POST] methods

    Returns:
        200 - If successful LIST return
        201 - If successful creation
        400 - Something happened validating data
        401 - Unauthorized
        404 - listing not found or unsuccessful LIST return
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
        if "listingID" in self.request.query_params:
            # We raise 404 is provided listing is not accurate for a particular listing
            listing = get_object_or_404(
                Listing, pk=self.request.query_params["listingID"]
            )
            # Only ACTIVE reservations
            queryset = ReservationListing.objects.filter(
                listing=listing, end_date__gte=now()
            )
        # Or IF we need ACTIVE reservations made on user's properties
        elif "user_properties" in self.request.query_params:
            queryset = ReservationListing.objects.filter(
                listing__creator=self.request.user, end_date__gte=now()
            )
        else:
            # IF we fail to get listingID or user_properties we then return all of the authenticated user's reservations (all times)
            queryset = ReservationListing.objects.filter(user=self.request.user)

        return queryset

    def create(self, request, *args, **kwargs):
        # Try to get full data from front-end
        try:
            data = {
                "listing": request.data["listingID"],
                "user": request.user.id,
                "start_date": request.data["start_date"],
                "end_date": request.data["end_date"],
            }
        except:
            # [ref] https://www.django-rest-framework.org/api-guide/exceptions/#parseerror
            raise ParseError
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ReservationDestroyView(DestroyAPIView):
    """
    View that handles destroying Reservation instances based on query_params

    Permission:
        User needs to be authenticated

    Accepts:
        [DELETE] method

    Returns:
        204 - Could delete object
        401 - Unauthorized
        404 - Could not delete object
    """

    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = ReservationListSerializer

    def get_queryset(self):
        # We're handling 2 scenarios: user that made the reservation OR owner of the property
        if "is_owner" in self.request.query_params:
            # So owners can cancel any particular renting
            return ReservationListing.objects.filter(listing__creator=self.request.user)
        # We make sure to filter the data based on loggedin user, so he is the owner!
        return ReservationListing.objects.filter(user=self.request.user)
