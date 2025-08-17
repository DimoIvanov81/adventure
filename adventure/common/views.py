from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

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


# My Events Views For The Card My Events --------------------------------------------------------

class MyEventsView(LoginRequiredMixin, TemplateView):
    template_name = "common/my_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        context["active_events"] = active
        context["expired_events"] = expired
        context["total_events_count"] = len(active) + len(expired)
        return context


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
        context = super().get_context_data(**kwargs)
        participants = (
            self.object.participations_to_event
            .select_related("user")
            .order_by("-date_joined")
        )
        context["participants"] = participants
        context["participants_count"] = participants.count()
        context["emails_list"] = ", ".join(
            (p.contact_email or p.user.email) for p in participants
            if (p.contact_email or p.user.email)
        )
        return context


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
    return redirect("my_event_comments", pk=event.pk)


# My Tracks Views For The Card My Tracks --------------------------------------------------------

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
        context = super().get_context_data(**kwargs)
        qs = context["tracks"]
        context["total_tracks"] = qs.paginator.count if hasattr(qs, "paginator") else qs.count()
        return context


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
        context = super().get_context_data(**kwargs)
        t = context["track"]
        context["average_rating"] = getattr(t, "average_rating", None) or getattr(t, "avg_rating", None)
        context["rating_count"] = getattr(t, "rating_count", None) or getattr(t, "ratings_count", 0)
        return context


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
        context = self.get_context_data()
        image_formset = context["image_formset"]

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return redirect("my_track_details", pk=self.object.pk)


        print("Formset errors:", image_formset.errors)
        print("Non-form errors:", image_formset.non_form_errors())

        context["form"] = form
        context["image_formset"] = image_formset
        return self.render_to_response(context)


@login_required
@require_POST
def my_track_delete(request, pk):
    track = get_object_or_404(MtbTracks, pk=pk, author=request.user)
    track.delete()
    return redirect('my_tracks')


# My Participations Views For The Card My Events I am attending ---------------------------------------

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
