from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_countries.widgets import CountrySelectWidget
import json

from .models import Brand, Wrestler, Championship, Event, Match, MatchType, TagTeam
from .forms import MatchForm, ChampionshipForm, TagTeamForm

class IndexView(generic.ListView):
	template_name = 'wwe2k16/brands.html'
	context_object_name = 'all_brands'

	def get_queryset(self):
		return Brand.objects.all().order_by('created_at')

class BrandView(generic.DetailView):
	model = Brand
	template_name = 'wwe2k16/brand.html'

class BrandCreate(CreateView):
	model = Brand
	fields = ['name', 'color']
	template_name = 'wwe2k16/forms/create/brand.html'

class BrandDelete(DeleteView):
	model = Brand
	success_url = reverse_lazy('wwe2k16:index')

class BrandUpdate(UpdateView):
	model = Brand
	fields = ['name']
	template_name = 'wwe2k16/forms/update/brand.html'

class WrestlersView(generic.ListView):
	template_name = 'wwe2k16/wrestlers.html'
	context_object_name = 'all_wrestlers'

	def get_queryset(self):
		return Wrestler.objects.all().order_by('name')

class WrestlerView(generic.DetailView):
	model = Wrestler
	template_name = 'wwe2k16/wrestler.html'

class WrestlerCreate(CreateView):
	model = Wrestler
	fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']
	widgets = {'country': CountrySelectWidget()}
	template_name = 'wwe2k16/forms/create/wrestler.html'

class WrestlerDelete(DeleteView):
	model = Wrestler
	success_url = reverse_lazy('wwe2k16:wrestlers')

class WrestlerUpdate(UpdateView):
	model = Wrestler
	fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']
	widgets = {'country': CountrySelectWidget()}
	template_name = 'wwe2k16/forms/update/wrestler.html'

class TagTeamsView(generic.ListView):
	template_name = 'wwe2k16/tag_teams.html'
	context_object_name = 'all_tag_teams'

	def get_queryset(self):
		return TagTeam.objects.all().order_by('name')

class TagTeamView(generic.DetailView):
	model = TagTeam
	template_name = 'wwe2k16/tag_team.html'

class TagTeamCreate(CreateView):
	form_class = TagTeamForm
	template_name = 'wwe2k16/forms/create/tag_team.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		request_dict = dict(request.POST.lists())
		members_list = []
		if u'members_list[]' in request_dict:
			members_list = request_dict[u'members_list[]']
		modified_members_list = [str(x) for x in members_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			tag_team = form.save(commit=False)
			tag_team.save()
			for x in modified_members_list:
				member = Wrestler.objects.get(name = x)
				tag_team.members.add(member)

		# FIXME: return a json response instead of sending render
		return render(request, self.template_name, {'form': form})

class TagTeamDelete(DeleteView):
	model = TagTeam
	success_url = reverse_lazy('wwe2k16:tagteams')

class TagTeamUpdate(UpdateView):
	model = TagTeam
	fields = ['name', 'members']
	template_name = 'wwe2k16/forms/update/tag_team.html'

class EventsView(generic.ListView):
	template_name = 'wwe2k16/events.html'
	context_object_name = 'all_events'

	def get_queryset(self):
		return Event.objects.all().order_by('name')

class EventView(generic.DetailView):
	model = Event
	template_name = 'wwe2k16/event.html'

class EventCreate(CreateView):
	model = Event
	fields = ['name', 'brand', 'year']
	template_name = 'wwe2k16/forms/create/event.html'

class EventDelete(DeleteView):
	model = Event
	success_url = reverse_lazy('wwe2k16:events')

class EventUpdate(UpdateView):
	model = Event
	fields = ['name', 'brand', 'year']
	template_name = 'wwe2k16/forms/update/event.html'

class ChampionshipsView(generic.ListView):
	template_name = 'wwe2k16/championships.html'
	context_object_name = 'all_championships'

	def get_queryset(self):
		return Championship.objects.all().order_by('created_at')

class ChampionshipView(generic.DetailView):
	model = Championship
	template_name = 'wwe2k16/championship.html'

class ChampionshipCreate(CreateView):
	form_class = ChampionshipForm
	template_name = 'wwe2k16/forms/create/championship.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		request_dict = dict(request.POST.lists())
		champions_list = []
		if u'champions_list[]' in request_dict:
			champions_list = request_dict[u'champions_list[]']
		modified_champions_list = [str(x) for x in champions_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			championship = form.save(commit=False)
			championship.save()
			for x in modified_champions_list:
				champion = Wrestler.objects.get(name = x)
				championship.champion.add(champion)

		# FIXME: return a json response instead of sending render
		return render(request, self.template_name, {'form': form})

class ChampionshipDelete(DeleteView):
	model = Championship
	success_url = reverse_lazy('wwe2k16:championships')

class ChampionshipUpdate(UpdateView):
	model = Championship
	fields = ['name', 'belt_type', 'champion']
	template_name = 'wwe2k16/forms/update/championship.html'

class MatchTypesView(generic.ListView):
	template_name = 'wwe2k16/match_types.html'
	context_object_name = 'all_match_types'

	def get_queryset(self):
		return MatchType.objects.all().order_by('name')

class MatchTypeView(generic.DetailView):
	model = MatchType
	template_name = 'wwe2k16/match_type.html'

class MatchTypeCreate(CreateView):
	model = MatchType
	fields = ['name', 'no_of_participants']
	template_name = 'wwe2k16/forms/create/match_type.html'

class MatchTypeDelete(DeleteView):
	model = MatchType
	success_url = reverse_lazy('wwe2k16:matchtypes')

class MatchTypeUpdate(UpdateView):
	model = MatchType
	fields = ['name', 'no_of_participants']
	template_name = 'wwe2k16/forms/update/match_type.html'

class MatchesView(generic.ListView):
	template_name = 'wwe2k16/matches.html'
	context_object_name = 'all_matches'

	def get_queryset(self):
		return Match.objects.all().order_by('event')

class MatchView(generic.DetailView):
	model = Match
	template_name = 'wwe2k16/match.html'

class MatchCreate(View):
	form_class = MatchForm
	template_name = 'wwe2k16/forms/create/match.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		request_dict = dict(request.POST.lists())
		participants_list = []
		if u'participants_list[]' in request_dict:
			participants_list = request_dict[u'participants_list[]']
		modified_participants_list = [str(x) for x in participants_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			match = form.save(commit=False)
			belt_type = match.championship.belt_type
			if belt_type == 'PR':
				match.winner.primary += 1
			elif belt_type == 'SE':
				match.winner.secondary += 1
			elif belt_type == 'TE':
				match.winner.tertiary += 1
			elif belt_type == 'TT':
				match.winner.tag_team += 1
			match.winner.save()
			match.save()
			for x in modified_participants_list:
				participant = Wrestler.objects.get(name = x)
				match.participants.add(participant)

		return render(request, self.template_name, {'form': form})

class MatchDelete(DeleteView):
	model = Match
	success_url = reverse_lazy('wwe2k16:matches')

class MatchUpdate(UpdateView):
	model = Match
	fields = ['event', 'match_type', 'participants']
	template_name = 'wwe2k16/forms/update/match.html'

class TagTeamMatchCreate(View):
	form_class = MatchForm
	template_name = 'wwe2k16/forms/create/tag_team_match.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		request_dict = dict(request.POST.lists())
		team1_list = request_dict[u'team1_list[]']
		team2_list = request_dict[u'team2_list[]']
		modified_team1_list = [str(x) for x in team1_list]
		modified_team2_list = [str(x) for x in team2_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			match = form.save(commit=False)
			winner = match.winner
			winning_team = []
			if winner == 1:
				winning_team = modified_team1_list
			elif winner == 2:
				winning_team = modified_team2_list
			for x in winning_team:
				wrestler = Wrestler.objects.get(name = x)
				wrestler.tag_team += 1
				wrestler.save()
			match.save()
			for x in modified_team1_list:
				participant = Wrestler.objects.get(name = x)
				match.team1.add(participant)
			for x in modified_team2_list:
				participant = Wrestler.objects.get(name = x)
				match.team2.add(participant)

		return render(request, self.template_name, {'form': form})

def get_wrestlers(request):
	mimetype = 'application/json'
	print(request.GET)
	if request.is_ajax():
		q = request.GET.get('term', '')
		wrestlers = Wrestler.objects.filter(name__icontains = q)
		results = []
		for wrestler in wrestlers:
			results.append(wrestler.name)
		data = json.dumps(results)
	else:
		data = 'fail'
	return HttpResponse(data, mimetype)
