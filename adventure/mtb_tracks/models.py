from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

from adventure.mtb_tracks.choices import TrackDifficulty
from adventure.mtb_tracks.validators import FileExtensionValidator, FileSizeValidator

UserModel = get_user_model()


class MtbTracks(models.Model):
    title = models.CharField(max_length=100)
    difficulty = models.CharField(
        max_length=10,
        choices=TrackDifficulty.choices,
        default=TrackDifficulty.Unknown
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='authors_tracks'
    )

    gps_file = models.FileField(
        upload_to='MTB/mtb_tracks',
        validators=[
            FileExtensionValidator(),
            FileSizeValidator(10),
        ],
        blank=True,
        null=True
    )
    description = models.TextField()

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def first_image(self):
        return self.images.first()

    class Meta:
        ordering = ('-date_created',)

    @property
    def average_rating(self):
        return self.ratings.aggregate(avg=Avg('rating'))['avg'] or 0


class TrackImages(models.Model):
    track = models.ForeignKey(
        MtbTracks,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='MTB/track_images',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png']),
            FileSizeValidator(5),
        ],
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )


class Comment(models.Model):
    track = models.ForeignKey(
        MtbTracks,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )

    text = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author.profile.full_name()} on {self.track.title}"
