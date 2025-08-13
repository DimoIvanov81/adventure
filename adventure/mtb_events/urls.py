from django.urls import path

from adventure.mtb_events.views import MtbEventListView, MtbEventDetailView, MtbEventCreateView, participate_event, \
    MtbEventUpdateView, MtbEventDeleteView, cancel_participation, add_event_comment, edit_event_comment, \
    delete_event_comment

urlpatterns = [
    path('explore-all-events/', MtbEventListView.as_view(), name='explore_all_events'),
    path('<int:pk>/event-details/', MtbEventDetailView.as_view(), name='event_details'),
    path('create-event/', MtbEventCreateView.as_view(), name='create_event'),

    path('<int:pk>/participate/', participate_event, name='participate_event'),
    path('<int:pk>/edit/', MtbEventUpdateView.as_view(), name='event_edit'),
    path("<int:pk>/cancel/", cancel_participation, name="cancel_participation"),
    path('<int:pk>/delete/', MtbEventDeleteView.as_view(), name='event_delete'),
    path('<int:pk>/comments/add/', add_event_comment, name='add_event_comment'),
    path('comments/<int:comment_id>/edit/', edit_event_comment, name='edit_event_comment'),
    path('comments/<int:comment_id>/delete/', delete_event_comment, name='delete_event_comment'),

]