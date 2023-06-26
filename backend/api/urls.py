from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.UserCreationView.as_view()),
    path('account/<str:key>/', views.RetrieveUserInformation.as_view()),
    path('auth/token_auth/', views.CustomAuthToken.as_view()),
]
