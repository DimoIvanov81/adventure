from django.db import models
from django.contrib.auth import get_user_model

from adventure.mtb_events.managers import MtbEventManager
from adventure.mtb_tracks.validators import FileExtensionValidator, FileSizeValidator

UserModel = get_user_model()


class MtbEvent(models.Model):
    title = models.CharField(max_length=100)  # here the author can write somthing like start and edn point

    description = models.TextField()  # Here the author should write about the program of the event and every step ao
    # the event for example -> the number of days, the stops for the evenings and so on

    start_date = models.DateField()

    contact_email = models.EmailField(blank=True, null=True)

    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    date_created = models.DateField(auto_now_add=True)

    organizer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} by {self.organizer}'

    objects = MtbEventManager()


class MtbEventImage(models.Model):
    event = models.ForeignKey(
        MtbEvent,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='MTB/event_pics',
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

    def __str__(self):
        return f"Image for {self.event.title}"


class Participation(models.Model):
    event = models.ForeignKey(
        MtbEvent,
        on_delete=models.CASCADE,
        related_name='participations_to_event'  # gives us a queryset of Participation's objects for this event from
        # which we can get the count of user or the user itself who have joined the event
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='participations_to_user'  # gives us the events for which the user has been signed
    )

    contact_email = models.EmailField(
        blank=True,
        null=True)

    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    questions = models.TextField(
        blank=True,
        null=True
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='unique_event_participant')
        ]

    def __str__(self):
        return f"{self.user} in {self.event.title}"


class EventComment(models.Model):
    event = models.ForeignKey(
        MtbEvent,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='event_comments'
    )

    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.event.title}"


"""
    my_events = request.user.organized_events.all()
    for event in my_events:
    pending = event.comments.filter(is_visible=False)

    from django.contrib.auth.decorators import login_required
    from django.shortcuts import render

    @login_required
    def my_events_dashboard(request):
        events = request.user.organized_events.all()
        context = {
            "events": events,
        }
        return render(request, "events/my_events_dashboard.html", context)
"""
