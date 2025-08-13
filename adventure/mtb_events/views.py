from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from adventure.mtb_events.mixins import OwnerOrStaffRequiredMixin
from adventure.mtb_events.models import MtbEvent, Participation, EventComment
from adventure.mtb_events.forms import (
    MtbEventForm,
    MtbEventImageFormSet,
    ParticipationForm,
    EventCommentForm,
)


class MtbEventListView(ListView):
    model = MtbEvent
    template_name = "events/event_list.html"
    context_object_name = "events"
    paginate_by = 6

    def get_queryset(self):
        return (
            MtbEvent.objects.active()
            .filter(is_published=True)
            .order_by("-date_created")
        )


class MtbEventDetailView(DetailView):
    model = MtbEvent
    template_name = "events/event_detail.html"
    context_object_name = "event"
    queryset = (
        MtbEvent.objects
        .select_related("organizer")
        .prefetch_related("images", "participations_to_event__user", "comments__author")
    )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        event = self.object
        participants = event.participations_to_event.all()

        ctx["images"] = event.images.all()
        ctx["participants"] = participants
        ctx["participants_count"] = participants.count()

        user = self.request.user
        ctx["is_participating"] = (
                user.is_authenticated and participants.filter(user=user).exists()
        )
        return ctx


class MtbEventCreateView(LoginRequiredMixin, CreateView):
    model = MtbEvent
    form_class = MtbEventForm
    template_name = "events/event_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = MtbEventImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            context["image_formset"] = MtbEventImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]

        if image_formset.is_valid():
            form.instance.organizer = self.request.user
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("event_details", kwargs={"pk": self.object.pk})


class MtbEventUpdateView(LoginRequiredMixin, OwnerOrStaffRequiredMixin, UpdateView):
    model = MtbEvent
    form_class = MtbEventForm
    template_name = "events/event_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        if self.request.POST:
            context["image_formset"] = MtbEventImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["image_formset"] = MtbEventImageFormSet(instance=self.object)
        context["is_edit"] = True
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("event_details", kwargs={"pk": self.object.pk})


class MtbEventDeleteView(LoginRequiredMixin, OwnerOrStaffRequiredMixin, DeleteView):
    model = MtbEvent
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("explore_all_events")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Събитието беше изтрито.")
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def participate_event(request, pk):
    event = get_object_or_404(MtbEvent, pk=pk)
    form = ParticipationForm(request.POST)
    if form.is_valid():
        part, created = Participation.objects.get_or_create(
            event=event,
            user=request.user,
            defaults=form.cleaned_data,
        )
        if not created:
            for f, v in form.cleaned_data.items():
                setattr(part, f, v)
            part.save()
        messages.success(request, "Записа за участие е успешен.")
    return redirect("event_details", pk=pk)


@login_required
@require_http_methods(["GET", "POST"])
def add_event_comment(request, pk):
    event = get_object_or_404(MtbEvent, pk=pk)

    if request.method == "POST":
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            return redirect(_back_to_event_comments(event.pk))
    else:
        form = EventCommentForm()

    context = {
        "form": form,
        "event": event,
    }
    return render(request, "events/comment_form.html", context)


def _back_to_event_comments(event_pk: int) -> str:
    return f"{reverse('event_details', kwargs={'pk': event_pk})}#comments"


@login_required
@require_http_methods(["GET", "POST"])
def edit_event_comment(request, comment_id):
    comment = get_object_or_404(EventComment, pk=comment_id)
    if request.user != comment.author and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = EventCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Коментарът е обновен.")
            return redirect(
                f"{reverse('event_details', kwargs={'pk': comment.event.pk})}#comment-{comment.pk}"
            )
    else:
        form = EventCommentForm(instance=comment)

    return render(
        request, "events/comment_form.html", {"form": form, "event": comment.event}
    )


@login_required
@require_POST
def delete_event_comment(request, comment_id):
    comment = get_object_or_404(EventComment, pk=comment_id)
    if request.user != comment.author and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    event_pk = comment.event.pk
    comment.delete()
    messages.success(request, "Коментарът е изтрит.")
    return redirect(_back_to_event_comments(event_pk))


@login_required
@require_POST
def cancel_participation(request, pk):
    event = get_object_or_404(MtbEvent, pk=pk)
    Participation.objects.filter(event=event, user=request.user).delete()
    messages.success(request, "Вашето участие е отменено.")
    return redirect("event_details", pk=pk)
