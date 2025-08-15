from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView, ListView, DetailView
from adventure.mtb_tracks.forms import MtbTrackForm, TrackImageFormSet, TrackCommentForm
from adventure.mtb_tracks.models import MtbTracks, Comment
from adventure.ratings.models import MtbTrackRating


class ExploreTracks(ListView):
    model = MtbTracks
    template_name = 'tracks/explore_tracks.html'
    context_object_name = 'tracks'
    paginate_by = 6

    def get_queryset(self):
        return MtbTracks.objects.filter(is_published=True).prefetch_related('images')


class TrackCreationView(LoginRequiredMixin, CreateView):
    model = MtbTracks
    form_class = MtbTrackForm
    template_name = 'tracks/create_track.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['image_formset'] = TrackImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = TrackImageFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']

        if image_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()

            image_formset.instance = self.object
            image_formset.save()

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TrackDetailView(DetailView):
    model = MtbTracks
    template_name = 'tracks/track_detail.html'
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        track = self.get_object()

        context['images'] = track.images.all()
        context['comments'] = track.comments.filter(is_visible=True).order_by('-date_created')
        context['average_rating'] = round(track.average_rating or 0, 1)
        context['rating_count'] = track.ratings.count()

        if self.request.user.is_authenticated:
            try:
                rating = track.ratings.get(user=self.request.user)
                context['user_rating'] = rating.rating
            except MtbTrackRating.DoesNotExist:
                context['user_rating'] = 0

        return context


@login_required
@require_http_methods(["GET", "POST"])
def add_comment(request, pk):
    track = get_object_or_404(MtbTracks, pk=pk)

    if request.method == "POST":
        form = TrackCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.track = track
            comment.author = request.user
            comment.save()
            return redirect(reverse('track_detail', kwargs={'pk': track.pk}))
    else:
        form = TrackCommentForm()

    context = {
        'form': form,
        'track': track
    }

    return render(request, 'tracks/comment_form.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = TrackCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated.")
            return redirect(f"{reverse('track_detail', kwargs={'pk': comment.track.pk})}#comment-{comment.pk}")
    else:
        form = TrackCommentForm(instance=comment)

    return render(request, 'tracks/comment_form.html', {'form': form, 'track': comment.track})


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author and not request.user.is_staff:
        return HttpResponseForbidden("Not allowed")

    track_pk = comment.track.pk
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect(f"{reverse('track_detail', kwargs={'pk': track_pk})}#comments")
