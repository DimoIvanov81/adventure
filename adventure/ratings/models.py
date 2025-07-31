from django.db import models
from django.contrib.auth import get_user_model
from adventure.mtb_tracks.models import MtbTracks

UserModel = get_user_model()


class MtbTrackRating(models.Model):
    track = models.ForeignKey(
        MtbTracks,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='track_ratings'
    )

    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['track', 'user'], name='unique_track_user_rating')
        ]

    def __str__(self):
        return f"{self.user} rated {self.track.title} with {self.rating}"
