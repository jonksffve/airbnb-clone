from rest_framework.serializers import ModelSerializer, ValidationError, DecimalField
from .models import Listing, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ListingSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'price', 'guestCount',
                  'roomCount', 'bathroomCount', 'category', 'location']
