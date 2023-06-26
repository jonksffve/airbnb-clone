from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.UserCreationView.as_view()),
    path('account/auth/', views.CustomAuthToken.as_view()),
]
