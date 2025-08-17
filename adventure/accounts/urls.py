from django.contrib.auth.views import LogoutView
from django.urls import path

from adventure.accounts.views import RegisterView, ProfileUpdateView, UserLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]