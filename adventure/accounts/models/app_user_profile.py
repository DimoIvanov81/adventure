
from django.contrib.auth import get_user_model
from django.db import models

from adventure.mtb_tracks.validators import FileExtensionValidator, FileSizeValidator

UserModel = get_user_model()


class AppProfile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png']),
            FileSizeValidator(5),
        ],
        blank=True,
        null=True)
    bio = models.TextField(blank=True, null=True)

    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.user.email

    @property
    def date_joined(self):

        return self.user.date_joined

    def __str__(self):
        return self.full_name()

