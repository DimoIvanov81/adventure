from django.urls import path

from adventure.mtb_tracks.views import TrackCreationView, ExploreTracks, add_comment, TrackDetailView, edit_comment, \
    delete_comment
   

urlpatterns = [
    path('create/', TrackCreationView.as_view(), name='create_track'),
    path('explore/', ExploreTracks.as_view(), name='explore_tracks'),
    path('<int:pk>/', TrackDetailView.as_view(), name='track_detail'),
    path('<int:pk>/comment/', add_comment, name='track_add_comment'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='comment_edit'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='comment_delete'),
]