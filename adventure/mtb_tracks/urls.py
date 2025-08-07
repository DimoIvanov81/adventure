from django.urls import path

from adventure.mtb_tracks.views import TrackCreationView

urlpatterns = [
    path('create/', TrackCreationView.as_view(), name='create_track'),
]