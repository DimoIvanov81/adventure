from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DetailView, ListView, UpdateView


from adventure.mtb_events.models import MtbEvent, EventComment
from adventure.mtb_tracks.forms import MtbTrackForm, TrackImageFormSet
from adventure.mtb_tracks.models import MtbTracks

UserModel = get_user_model()


def home(request):
    return render(request, "common/home.html")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "common/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        my_events = MtbEvent.objects.filter(organizer=user).prefetch_related("participations_to_event", "images")

        participating_events = MtbEvent.objects.filter(participations_to_event__user=user).distinct()

        my_tracks = MtbTracks.objects.filter(author=user).prefetch_related("images")

        my_event_comments = EventComment.objects.filter(event__organizer=user).select_related("author", "event")

        context["my_events"] = my_events
        context["participating_events"] = participating_events
        context["my_tracks"] = my_tracks
        context["my_event_comments"] = my_event_comments

        return context


class MyEventsView(LoginRequiredMixin, TemplateView):
    template_name = "common/my_events.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        all_events = (
            MtbEvent.objects
            .filter(organizer=user)
            .prefetch_related("participations_to_event__user", "images")
            .annotate(
                comments_count=Count("comments", distinct=True),
                participants_count=Count("participations_to_event", distinct=True),
            )
            .order_by("-start_date", "-date_created")
        )

        def wrap(e):

            emails = [p.user.email for p in e.participations_to_event.all()]
            return {
                "event": e,
                "participant_count": e.participants_count,
                "participant_emails": emails,
                "comments_count": e.comments_count,
            }

        active = [wrap(e) for e in all_events.active()]
        expired = [wrap(e) for e in all_events.expired()]

        ctx["active_events"] = active
        ctx["expired_events"] = expired
        ctx["total_events_count"] = len(active) + len(expired)
        return ctx


class MyEventParticipantsView(LoginRequiredMixin, DetailView):
    model = MtbEvent
    template_name = "common/my_event_participants.html"
    context_object_name = "event"

    def get_queryset(self):
        return (
            MtbEvent.objects
            .filter(organizer=self.request.user)
            .prefetch_related("participations_to_event__user")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        participants = self.object.participations_to_event.all()
        ctx["participants"] = participants
        ctx["participants_count"] = participants.count()
        ctx["emails_list"] = ", ".join(p.user.email for p in participants)
        return ctx


class MyEventCommentsView(LoginRequiredMixin, DetailView):
    model = MtbEvent
    template_name = "common/my_event_comments.html"
    context_object_name = "event"

    def get_queryset(self):
        return (
            MtbEvent.objects
            .filter(organizer=self.request.user)
            .prefetch_related("comments__author")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author").order_by("-date_created")
        ctx["comments_count"] = ctx["comments"].count()
        return ctx


@login_required
def moderate_delete_event_comment(request, pk, comment_id):
    event = get_object_or_404(MtbEvent, pk=pk, organizer=request.user)
    comment = get_object_or_404(EventComment, pk=comment_id, event=event)
    if request.method != "POST":
        return HttpResponseForbidden("Not allowed")
    comment.delete()
    messages.success(request, "Коментарът е изтрит.")
    return redirect("my_event_comments", pk=event.pk)


class MyTracksView(LoginRequiredMixin, ListView):
    template_name = "common/my_tracks.html"
    context_object_name = "tracks"
    paginate_by = 9

    def get_queryset(self):
        return (
            MtbTracks.objects
            .filter(author=self.request.user)
            .prefetch_related("images")
            .annotate(
                avg_rating=Avg("ratings__rating"),
                ratings_count=Count("ratings")
            )
            .order_by("-date_created")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = ctx["tracks"]
        ctx["total_tracks"] = qs.paginator.count if hasattr(qs, "paginator") else qs.count()
        return ctx


class MyTrackDetailsView(LoginRequiredMixin, DetailView):
    model = MtbTracks
    template_name = 'common/my_track_details.html'
    context_object_name = "track"

    def get_queryset(self):
        return (
            MtbTracks.objects
            .filter(author=self.request.user)
            .prefetch_related("images")
            .annotate(
                avg_rating=Avg("ratings__rating"),
                ratings_count=Count("ratings")
            )
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        t = ctx["track"]
        ctx["average_rating"] = getattr(t, "average_rating", None) or getattr(t, "avg_rating", None)
        ctx["rating_count"] = getattr(t, "rating_count", None) or getattr(t, "ratings_count", 0)
        return ctx


class MyTrackUpdateView(LoginRequiredMixin, UpdateView):
    model = MtbTracks
    form_class = MtbTrackForm
    template_name = "tracks/create_track.html"
    context_object_name = "track"

    def get_queryset(self):
        return MtbTracks.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["image_formset"] = TrackImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            ctx["image_formset"] = TrackImageFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        image_formset = ctx["image_formset"]
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return redirect("my_track_details", pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))


@login_required
@require_POST
def my_track_delete(request, pk):
    track = get_object_or_404(MtbTracks, pk=pk, author=request.user)
    title = track.title
    track.delete()
    messages.success(request, f'Тракът „{title}“ беше изтрит.')
    return redirect('my_tracks')


class MyJoinedEventsView(LoginRequiredMixin, ListView):
    template_name = "common/my_joined_events.html"
    context_object_name = "events"
    paginate_by = 6

    def get_queryset(self):
        return (
            MtbEvent.objects
            .filter(participations_to_event__user=self.request.user)
            .prefetch_related("images", "organizer")
            .annotate(
                participants_count=Count("participations_to_event", distinct=True),
                comments_count=Count("comments", distinct=True),
            )
            .order_by("-start_date", "-date_created")
            .distinct()
        )
