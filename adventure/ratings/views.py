from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from adventure.mtb_tracks.models import MtbTracks
from adventure.ratings.models import MtbTrackRating
import json


class RateTrackView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required")

        track = get_object_or_404(MtbTracks, pk=pk)

        try:
            data = json.loads(request.body)
            rating_value = int(data.get('rating'))
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data")

        if rating_value not in range(1, 6):
            return HttpResponseBadRequest("Rating must be between 1 and 5")

        rating_obj, created = MtbTrackRating.objects.update_or_create(
            track=track,
            user=request.user,
            defaults={'rating': rating_value}
        )

        average = track.average_rating
        count = track.ratings.count()

        return JsonResponse({
            'message': 'Rating submitted',
            'average_rating': round(average, 2),
            'ratings_count': count,
            'user_rating': rating_value,
        })
