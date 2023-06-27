from rest_framework.generics import CreateAPIView, RetrieveAPIView
from accounts.serializers import UserSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response

user_model = get_user_model()


class UserCreationView(CreateAPIView):
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


class RetrieveUserInformation(RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'key'
