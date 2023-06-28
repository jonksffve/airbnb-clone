from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.UserCreateView.as_view()),
    path('account/<str:key>/', views.UserRetrieveView.as_view()),
    path('auth/token_auth/', views.CustomAuthToken.as_view()),
    path('listing/', views.ListingCreateView.as_view()),
]
