from rest_framework.generics import CreateAPIView
from accounts.models import User
from accounts.serializers import UserSerializer


class UserCreationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
