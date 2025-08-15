from django import forms
from django.forms import inlineformset_factory

from adventure.mtb_events.models import MtbEvent, MtbEventImage, Participation, EventComment
from adventure.mtb_tracks.mixins import PlaceholderFormMixin


class MtbEventForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = MtbEvent
        fields = ['title', 'description', 'start_date', 'contact_email', 'contact_phone']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }

    placeholders = {
        'title': 'Enter the title of the event',
        'description': 'Describe the program of the event',
        'start_date': 'Select the start of the event date (YYYY-MM-DD)',
        'contact_email': 'Contact email',
        'contact_phone': 'Contact phone number',
    }


class MtbEventImageForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = MtbEventImage
        fields = ['image', 'description']

    placeholders = {
        'image': 'Upload an image (jpeg, jpg, png)',
        'description': 'You can add some words about this photo',
    }

    widgets = {
        'image': forms.ClearableFileInput(),
    }


MtbEventImageFormSet = inlineformset_factory(
    MtbEvent,
    MtbEventImage,
    form=MtbEventImageForm,
    extra=1,
    can_delete=True,
)


class ParticipationForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['contact_email', 'contact_phone', 'questions']

    placeholders = {
        'contact_email': 'Your email for contact',
        'contact_phone': 'Your phone number',
        'questions': 'Any questions about the event?',
    }


class EventCommentForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ['text']

    placeholders = {
        'text': 'Write your comment or question about the event',
    }
