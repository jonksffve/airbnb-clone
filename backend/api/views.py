from rest_framework.generics import (CreateAPIView,
                                     ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import UserSerializer, TokenSerializer
from .serializers import ListingSerializer

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Listing, Category

user_model = get_user_model()


class UserCreateView(CreateAPIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    queryset = user_model.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):
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
    permission_classes = [IsAuthenticated]
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'


class ListingCreateListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def create(self, request, *args, **kwargs):
        try:
            category_name = request.data['category']
        except:
            category_name = None
        category_obj = get_object_or_404(
            Category, name=category_name)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, category_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, category_obj):
        serializer.save(creator=self.request.user, category=category_obj)
