from .models import Wrestler, Championship, Event, Match, MatchType
from django import forms, template

class WrestlerForm(forms.ModelForm):
    fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']

    def __init__(self, *args, **kwargs):
        super(WrestlerForm, self).__init__(*args, **kwargs)
        self.fields['brand'].empty_label = ''

    class Meta:
        model = Wrestler
        fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']

class ChampionshipForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = ['name', 'belt_type', 'champion']

class MatchForm(forms.ModelForm):
    fields = ['event', 'championship', 'match_type', 'participants', 'winner']

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['championship'].empty_label = ''

    class Meta:
        model = Match
        fields = ['event', 'championship', 'match_type', 'participants', 'winner']