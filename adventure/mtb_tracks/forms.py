from django import forms
from django.forms import inlineformset_factory

from adventure.mtb_tracks.mixins import PlaceholderFormMixin
from adventure.mtb_tracks.models import MtbTracks, TrackImages, Comment


class MtbTrackForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = MtbTracks
        fields = ['title', 'difficulty', 'gps_file', 'description', ]

        placeholders = {
            'title': 'Enter the title of your track',
            'difficulty': 'Select difficulty',
            'gps_file': 'Upload GPX/KML/TCX file',
            'description': 'Describe your track in maximum 200 rows',
        }

        widgets = {
            'difficulty': forms.Select(),
            'gps_file': forms.ClearableFileInput(),
            'description': forms.Textarea(attrs={'rows': 200}),
        }


class TrackImageForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = TrackImages
        fields = ['image', 'description']

        placeholders = {
            'image': 'Select (jpeg, jpg or png) image ',
            'description': 'You can add some words for the photo you are uploading',
        }

        widgets = {
            'image': forms.ClearableFileInput(),
        }


TrackImageFormSet = inlineformset_factory(
    MtbTracks,
    TrackImages,
    form=TrackImageForm,
    extra=1,
    can_delete=True,
)


class TrackCommentForm(PlaceholderFormMixin, forms.ModelForm):
    placeholders = {
        'text': 'You can add some words about what you think',
    }
    class Meta:
        model = Comment
        fields = ['text']


