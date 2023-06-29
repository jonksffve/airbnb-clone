from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Listing, Category, FavoriteListing
from accounts.serializers import UserSerializer


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


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = FavoriteListing
        fields = ['id', 'listing', 'user']
