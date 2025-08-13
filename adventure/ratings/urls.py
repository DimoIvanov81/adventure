from django.urls import path

from adventure.ratings.views import RateTrackView

urlpatterns = [
    path('<int:pk>/rate/', RateTrackView.as_view(), name='mtb-rating'),
]