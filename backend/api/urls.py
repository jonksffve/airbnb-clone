from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.UserCreateView.as_view()),
    path('account/<str:key>/', views.UserRetrieveView.as_view()),
    path('auth/token_auth/', views.CustomAuthToken.as_view()),
    path('listing/', views.ListingCreateListView.as_view()),
    path('listing/favorite/', views.FavoriteCreateView.as_view()),

    ##### TESTS DONE UNTIL THIS POINT #######

    path('listing/<str:pk>/', views.ListingRetrieveView.as_view()),
    ##### TESTS DONE UNTIL THIS POINT #######

    path('listing/favorite/<str:listing>/',
         views.FavoriteDestroyView.as_view())
]
