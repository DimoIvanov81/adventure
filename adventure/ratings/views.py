from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from adventure.mtb_tracks.models import MtbTracks
from adventure.ratings.forms import MtbTrackRatingForm
from adventure.ratings.models import MtbTrackRating


@login_required
@require_POST
def rate_track(request, pk):
    track = get_object_or_404(MtbTracks, pk=pk)
    form = MtbTrackRatingForm(request.POST)
    if form.is_valid():
        MtbTrackRating.objects.update_or_create(
            track=track,
            user=request.user,
            defaults={'rating': form.cleaned_data['rating']},
        )

    return redirect('track_detail', pk=pk)
