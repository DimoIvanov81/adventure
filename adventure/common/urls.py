from django.urls import path

from adventure.common import views
from adventure.common.views import DashboardView, MyEventsView, MyEventParticipantsView, MyEventCommentsView, \
    moderate_delete_event_comment, MyTracksView, MyTrackDetailsView, MyTrackUpdateView, my_track_delete, \
    MyJoinedEventsView


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('my-events/', MyEventsView.as_view(), name='my-events'),
    path("my-event/<int:pk>/participants/", MyEventParticipantsView.as_view(), name="event_participants"),
    path("my-event/<int:pk>/comments/", MyEventCommentsView.as_view(), name="my_event_comments"),
    path("my-event/<int:pk>/comments/<int:comment_id>/delete/", moderate_delete_event_comment,
         name="my_event_comment_delete"),
    path("my-tracks/", MyTracksView.as_view(), name="my_tracks"),
    path('my-track-details/<int:pk>/', MyTrackDetailsView.as_view(), name='my_track_details'),
    path("my-track-edit/<int:pk>/", MyTrackUpdateView.as_view(), name="my_track_edit"),
    path('my-track-delete/<int:pk>/', my_track_delete, name='my_track_delete'),
    path("my-joined-events/", MyJoinedEventsView.as_view(), name="my_joined_events"),


]




