from .models import Wrestler, TagTeam, Championship, Event, Match, TagTeamMatch, MatchType
from django.forms import ModelForm, TextInput, CharField, HiddenInput

class WrestlerForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(WrestlerForm, self).__init__(*args, **kwargs)
		self.fields['brand'].empty_label = ''

	class Meta:
		model = Wrestler
		fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']

class TagTeamForm(ModelForm):
	class Meta:
		model = TagTeam
		fields = ['name', 'members']

class ChampionshipForm(ModelForm):
	class Meta:
		model = Championship
		fields = ['name', 'belt_type', 'status', 'champion']

class MatchForm(ModelForm):
	def __init__(self, *args, **kwargs):
		exclude_event = kwargs.pop('exclude_event', None)
		super(MatchForm, self).__init__(*args, **kwargs)
		self.fields['event'].empty_label = ''
		self.fields['championship'].empty_label = ''
		self.fields['match_type'].empty_label = ''
		self.fields['winner'] = CharField(required=False, widget=TextInput(attrs={'class': 'autocomplete'}))
		if exclude_event:
			self.fields['event'].widget = HiddenInput()

	class Meta:
		model = Match
		fields = ['event', 'championship', 'match_type', 'participants']
		
class TagMatchForm(ModelForm):
	def __init__(self, *args, **kwargs):
		exclude_event = kwargs.pop('exclude_event', None)
		super(TagMatchForm, self).__init__(*args, **kwargs)
		self.fields['event'].empty_label = ''
		self.fields['championship'].empty_label = ''
		if exclude_event:
			self.fields['event'].widget = HiddenInput()

	class Meta:
		model = TagTeamMatch
		fields = ['event', 'championship', 'team1', 'team2', 'winner']