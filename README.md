## Apps
- [common](#common)
- [mtb_tracks](#mtb_tracks)
- [mtb_events](#mtb_events)

---

### common
- **Folder:** [adventure/common/](adventure/common/)
- **Models:** none

- `home` — public home page.  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/home.html](templates/common/home.html)

- `DashboardView` — logged-in user dashboard.  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/dashboard.html](templates/common/dashboard.html)

- `MyEventsView` — “My Events” (Active / Expired / All).  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/my_events.html](templates/common/my_events.html)

- `MyEventParticipantsView` — participants for my event.  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/my_event_participants.html](templates/common/my_event_participants.html)

- `MyEventCommentsView` — comments for my event.  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/my_event_comments.html](templates/common/my_event_comments.html)

- `moderate_delete_event_comment` — delete a comment from my event (POST).  
  Code: [views.py](adventure/common/views.py)

- `MyTracksView` — my tracks list (paginated) with avg rating & count.  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/my_tracks.html](templates/common/my_tracks.html)

- `MyTrackDetailsView` — my track details (avg rating & count).  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/my_track_details.html](templates/common/my_track_details.html)

- `MyTrackUpdateView` — edit my track (+ images formset).  
  Code: [views.py](adventure/common/views.py) · Template: [templates/tracks/create_track.html](templates/tracks/create_track.html)

- `my_track_delete` — delete my track (POST).  
  Code: [views.py](adventure/common/views.py)

- `MyJoinedEventsView` — events I’ve joined (paginated).  
  Code: [views.py](adventure/common/views.py) · Template: [templates/common/my_joined_events.html](templates/common/my_joined_events.html)

---

### mtb_tracks
- **Folder:** [adventure/mtb_tracks/](adventure/mtb_tracks/)
- **Views:** [views.py](adventure/mtb_tracks/views.py)

- `ExploreTracks` — public list of published tracks (pagination; prefetch images).  
  Code: [views.py](adventure/mtb_tracks/views.py) · Template: [templates/tracks/explore_tracks.html](templates/tracks/explore_tracks.html)

- `TrackDetailView` — public track details (images, visible comments, average rating, rating count; shows user rating if logged-in).  
  Code: [views.py](adventure/mtb_tracks/views.py) · Template: [templates/tracks/track_detail.html](templates/tracks/track_detail.html)

- `TrackCreationView` — create a new track (login required) with images formset; redirects on success.  
  Code: [views.py](adventure/mtb_tracks/views.py) · Template: [templates/tracks/create_track.html](templates/tracks/create_track.html)

- `track_comment` — add a comment to a track (login required); GET shows form, POST saves and redirects to the track.  
  Code: [views.py](adventure/mtb_tracks/views.py) · Template: [templates/tracks/comment_create.html](templates/tracks/comment_create.html)

- `add_comment` — add a comment to a track (login required); alternative form flow; GET/POST.  
  Code: [views.py](adventure/mtb_tracks/views.py) · Template: [templates/tracks/comment_form.html](templates/tracks/comment_form.html)

- `edit_comment` — edit an existing comment (login required; author or staff); GET pre-filled form; POST saves and anchors to the updated comment.  
  Code: [views.py](adventure/mtb_tracks/views.py) · Template: [templates/tracks/comment_form.html](templates/tracks/comment_form.html)

- `delete_comment` — delete a comment (login required; author or staff; POST only); redirects back to the track’s comments.  
  Code: [views.py](adventure/mtb_tracks/views.py)

---

### mtb_events
- **Folder:** [adventure/mtb_events/](adventure/mtb_events/)
- **Views:** [views.py](adventure/mtb_events/views.py)

- `MtbEventListView` — public list of active & published events, newest first (paginated).  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/event_list.html](templates/events/event_list.html)

- `MtbEventDetailView` — public event details with organizer, images, participants (+count), and `is_participating` for the current user.  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/event_detail.html](templates/events/event_detail.html)

- `MtbEventCreateView` — create a new event (login required) with image formset; redirects to details.  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/event_form.html](templates/events/event_form.html)

- `MtbEventUpdateView` — edit an event (login required, owner or staff), supports image formset; redirects to details.  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/event_form.html](templates/events/event_form.html)

- `MtbEventDeleteView` — delete an event (login required, owner or staff); success message; redirects to explore page.  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/event_confirm_delete.html](templates/events/event_confirm_delete.html)

- `participate_event` — join/update participation (POST, login required); creates or updates participation; success message; redirect to details.  
  Code: [views.py](adventure/mtb_events/views.py)

- `cancel_participation` — cancel participation (POST, login required); deletes current user’s participation; success message; redirect to details.  
  Code: [views.py](adventure/mtb_events/views.py)

- `add_event_comment` — add a comment (GET/POST, login required); on success anchors back to comments on the details page.  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/comment_form.html](templates/events/comment_form.html)

- `edit_event_comment` — edit a comment (GET/POST, login required; author or staff only); anchors to the updated comment on success.  
  Code: [views.py](adventure/mtb_events/views.py) · Template: [templates/events/comment_form.html](templates/events/comment_form.html)

- `delete_event_comment` — delete a comment (POST, login required; author or staff only); success message; anchors back to comments.  
  Code: [views.py](adventure/mtb_events/views.py)
