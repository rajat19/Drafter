from .models import Wrestler, TagTeam, Championship, Event, Match, TagTeamMatch, MatchType
from django import forms, template

class WrestlerForm(forms.ModelForm):
	fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']

	def __init__(self, *args, **kwargs):
		super(WrestlerForm, self).__init__(*args, **kwargs)
		self.fields['brand'].empty_label = ''

	class Meta:
		model = Wrestler
		fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']

class TagTeamForm(forms.ModelForm):
	class Meta:
		model = TagTeam
		fields = ['name', 'members']

class ChampionshipForm(forms.ModelForm):
	class Meta:
		model = Championship
		fields = ['name', 'belt_type', 'status', 'champion']

class MatchForm(forms.ModelForm):
	fields = ['event', 'championship', 'match_type', 'participants', 'winner']

	def __init__(self, *args, **kwargs):
		super(MatchForm, self).__init__(*args, **kwargs)
		self.fields['event'].empty_label = ''
		self.fields['championship'].empty_label = ''
		self.fields['match_type'].empty_label = ''
		self.fields['winner'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'autocomplete'}))

	class Meta:
		model = Match
		fields = ['event', 'championship', 'match_type', 'participants']

class TagMatchForm(forms.ModelForm):
	fields = ['event', 'championship', 'team1', 'team2', 'winner']

	def __init__(self, *args, **kwargs):
		super(TagMatchForm, self).__init__(*args, **kwargs)
		self.fields['event'].empty_label = ''
		self.fields['championship'].empty_label = ''

	class Meta:
		model = TagTeamMatch
		fields = ['event', 'championship', 'team1', 'team2', 'winner']