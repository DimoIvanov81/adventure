from django.urls import path

from adventure.ratings.views import rate_track

urlpatterns = [
    path('<int:pk>/rate/', rate_track, name='mtb-rating'),
]