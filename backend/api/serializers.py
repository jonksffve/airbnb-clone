from rest_framework.serializers import ModelSerializer
from .models import Listing, Category
from accounts.serializers import UserSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ListingSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'image', 'price', 'guestCount',
                  'roomCount', 'bathroomCount', 'category', 'location', 'creator']
