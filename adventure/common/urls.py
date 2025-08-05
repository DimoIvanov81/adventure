from django.urls import path

from adventure.common import views

urlpatterns = [
    path('', views.home, name='home'),
]