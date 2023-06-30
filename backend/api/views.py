from rest_framework.generics import (CreateAPIView,
                                     ListCreateAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerOrStaff (deprecated, is done by QuerySets now)

from accounts.serializers import UserSerializer, TokenSerializer
from .serializers import ListingSerializer, FavoriteSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Listing, Category, FavoriteListing

# Get the current User model
user_model = get_user_model()


class UserCreateView(CreateAPIView):
    """
    Creates a new user with the given data.
    """
    # @accepts: only POST method
    queryset = user_model.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):
    """
    Returns valid credentials so user can log in.
    Also returns the authenticated user information for front-end usage.
    """
    # @accepts: only POST method
    queryset = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user, context={'request': request})
        return Response({
            'token': token.key,
            'user': serializer.data
        })


class UserRetrieveView(RetrieveAPIView):
    """
    Retrieve a single user information with the provided Token authentication value.
    """
    # @permissions: user needs to be authenticated
    # @accepts: GET method
    permission_classes = [IsAuthenticated]
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'


class ListingCreateListView(ListCreateAPIView):
    """
    Creates a new instance OR returns list of objects, depending on the method.
    """
    # @permissions: user needs to be authenticated
    # @accepts: GET, POST methods
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def create(self, request, *args, **kwargs):
        # Found that client side we can send the form without category.
        # This makes sure to checks before trying to process the form
        try:
            category_name = request.data['category']
        except:
            category_name = None
        # Make sure the category exists in the database
        category_obj = get_object_or_404(
            Category, name=category_name)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, category_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, category_obj):
        serializer.save(creator=self.request.user, category=category_obj)


class FavoriteCreateView(CreateAPIView):
    """
    Creates a new model instance of FavoriteListing
    """
    # @permissions: user needs to be authenticated
    # @accepts: POST methods
    permission_classes = [IsAuthenticated]
    queryset = FavoriteListing.objects.all()
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        listing = get_object_or_404(Listing, pk=request.data['listingID'])
        serializer = self.get_serializer(
            data={"listing": listing.id, "user": request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FavoriteDestroyView(DestroyAPIView):
    """
    Deletes a model instance of FavoriteListing
    """
    # @permissions: user needs to be authenticated and be the owner of the object itself (this is done by filtering querysets both for listing and user)
    # @accepts: DELETE methods
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = FavoriteSerializer
    lookup_field = 'listing'

    def get_queryset(self):
        # We make sure to filter the data based on loggedin user, so he is the owner!
        return FavoriteListing.objects.filter(user=self.request.user)


##### TESTS DONE UNTIL THIS POINT #######
class ListingRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
