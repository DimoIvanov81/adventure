from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from adventure.mtb_tracks.forms import MtbTrackForm, TrackImageFormSet, TrackCommentForm
from adventure.mtb_tracks.models import MtbTracks


class TrackCreationView(LoginRequiredMixin, CreateView):
    model = MtbTracks
    form_class = MtbTrackForm
    template_name = 'tracks/create_track.html'
    success_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # we get the form in the context

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

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def track_comment(request, pk):
    track = get_object_or_404(MtbTracks, pk=pk)

    if request.method == 'POST':
        form = TrackCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.track = track
            comment.save()
            return redirect('track_detail', pk=track.pk)
    else:
        form = TrackCommentForm()

    context = {
        'form': form,
        'track': track,
    }
    return render(request, 'tracks/comment_create.html', context)



