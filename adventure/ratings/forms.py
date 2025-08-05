from django import forms
from adventure.ratings.models import MtbTrackRating
from adventure.mtb_tracks.mixins import PlaceholderFormMixin


class MtbTrackRatingForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = MtbTrackRating
        fields = ['rating']


