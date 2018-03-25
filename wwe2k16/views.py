from django.core.management import call_command
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.utils import timezone
from django.views import generic
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_countries.widgets import CountrySelectWidget
import json

from .models import Brand, Wrestler, Championship, Event, Match, TagTeamMatch, MatchType, TagTeam, ChampionshipHistory, DraftHistory, TemporaryDraft
from .forms import MatchForm, ChampionshipForm, TagTeamForm, TagMatchForm

class IndexView(TemplateView):
	template_name='wwe2k16/index.html'

class BrandsView(generic.ListView):
	template_name = 'wwe2k16/brands.html'
	context_object_name = 'all_brands'

	def get_queryset(self):
		return Brand.objects.order_by('created_at')

class BrandView(generic.DetailView):
	model = Brand
	template_name = 'wwe2k16/brand.html'

class BrandCreate(CreateView):
	model = Brand
	fields = ['name', 'color']
	template_name = 'wwe2k16/forms/create/brand.html'

class BrandDelete(View):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'slug' in kwargs:
			slug = kwargs['slug']
			Brand.objects.get(slug=slug).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class BrandUpdate(UpdateView):
	model = Brand
	fields = ['name']
	template_name = 'wwe2k16/forms/update/brand.html'

class WrestlersView(generic.ListView):
	template_name = 'wwe2k16/wrestlers.html'
	context_object_name = 'all_wrestlers'

	def get_queryset(self):
		return Wrestler.objects.order_by('name')

class WrestlerView(generic.DetailView):
	model = Wrestler
	template_name = 'wwe2k16/wrestler.html'

class WrestlerCreate(CreateView):
	model = Wrestler
	fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']
	widgets = {'country': CountrySelectWidget()}
	template_name = 'wwe2k16/forms/create/wrestler.html'

class WrestlerDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'slug' in kwargs:
			slug = kwargs['slug']
			Wrestler.objects.get(slug=slug).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class WrestlerUpdate(UpdateView):
	model = Wrestler
	fields = ['name', 'ovr', 'country', 'brand', 'height', 'weight', 'original_primary', 'original_secondary', 'primary', 'secondary', 'tertiary', 'tag_team']
	widgets = {'country': CountrySelectWidget()}
	template_name = 'wwe2k16/forms/update/wrestler.html'

class TagTeamsView(generic.ListView):
	template_name = 'wwe2k16/tag_teams.html'
	context_object_name = 'all_tag_teams'

	def get_queryset(self):
		return TagTeam.objects.order_by('name')

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
		if 'members_list[]' in request_dict:
			members_list = request_dict['members_list[]']
		modified_members_list = [str(x) for x in members_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			tag_team = form.save(commit=False)
			tag_team.save()
			for x in modified_members_list:
				member = Wrestler.objects.get(name = x)
				tag_team.members.add(member)
			data = {
				'result': 1,
				'message': 'Successfully added the tag team',
			}
		else: data = {
				'result': 0,
				'errors': json.loads(form.errors.as_json()),
			}
		return JsonResponse(data)

class TagTeamDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'slug' in kwargs:
			slug = kwargs['slug']
			TagTeam.objects.get(slug=slug).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class TagTeamUpdate(UpdateView):
	model = TagTeam
	fields = ['name', 'members']
	template_name = 'wwe2k16/forms/update/tag_team.html'

class EventsView(generic.ListView):
	template_name = 'wwe2k16/events.html'
	context_object_name = 'all_events'

	def get_queryset(self):
		return Event.objects.order_by('created_at')

class EventView(View):
	model = Event
	template_name = 'wwe2k16/event.html'
	match_form_class = MatchForm
	tag_match_form_class = TagMatchForm
	def get(self, request, *args, **kwargs):
		slug = kwargs['slug']
		event = Event.objects.get(slug=slug)
		match_form = self.match_form_class(exclude_event=True, initial={'event': event.pk})
		tag_match_form = self.tag_match_form_class(exclude_event=True, initial={'event': event.pk})
		return render(request, self.template_name, {
			'event': event,
			'match_form': match_form,
			'tag_match_form': tag_match_form,
		})

class EventCreate(CreateView):
	model = Event
	fields = ['name', 'brand', 'year']
	template_name = 'wwe2k16/forms/create/event.html'

class EventDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'slug' in kwargs:
			slug = kwargs['slug']
			Event.objects.get(slug=slug).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class EventUpdate(UpdateView):
	model = Event
	fields = ['name', 'brand', 'year']
	template_name = 'wwe2k16/forms/update/event.html'

class ChampionshipsView(generic.ListView):
	template_name = 'wwe2k16/championships.html'
	context_object_name = 'all_championships'

	def get_queryset(self):
		return Championship.objects.order_by('created_at')

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
		if 'champions_list[]' in request_dict:
			champions_list = request_dict['champions_list[]']
		modified_champions_list = [str(x) for x in champions_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			try:
				championship = form.save(commit=False)
				championship.save()
				belt_type = championship.belt_type
				for x in modified_champions_list:
					champion = Wrestler.objects.get(name = x)
					championship.champion.add(champion)
					if belt_type == 'PR':
						champion.primary += 1
					elif belt_type == 'SE':
						champion.secondary += 1
					elif belt_type == 'TE':
						champion.tertiary += 1
					elif belt_type == 'TT':
						champion.tag_team += 1
					champion.save()
				data = {
					'result': 1,
					'message': 'Successfully added the championship',
				}
			except Exception as e:
				data = {
					'result': 1,
					'message': e.message,
				}
		else: data = {
				'result': 0,
				'errors': json.loads(form.errors.as_json()),
			}
		return JsonResponse(data)
		
class ChampionshipDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'slug' in kwargs:
			try:
				slug = kwargs['slug']
				Championship.objects.get(slug=slug).delete()
				message = 'deleted'
			except Exception as e:
				message = e.message
		return JsonResponse(message, safe=False)

class ChampionshipUpdate(UpdateView):
	model = Championship
	fields = ['name', 'belt_type', 'champion']
	template_name = 'wwe2k16/forms/update/championship.html'

class MatchTypesView(generic.ListView):
	template_name = 'wwe2k16/match_types.html'
	context_object_name = 'all_match_types'

	def get_queryset(self):
		return MatchType.objects.order_by('name')

class MatchTypeView(generic.DetailView):
	model = MatchType
	template_name = 'wwe2k16/match_type.html'

class MatchTypeCreate(CreateView):
	model = MatchType
	fields = ['name', 'no_of_participants']
	template_name = 'wwe2k16/forms/create/match_type.html'

class MatchTypeDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'slug' in kwargs:
			slug = kwargs['slug']
			MatchType.objects.get(slug=slug).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class MatchTypeUpdate(UpdateView):
	model = MatchType
	fields = ['name', 'no_of_participants']
	template_name = 'wwe2k16/forms/update/match_type.html'

class MatchesView(generic.ListView):
	template_name = 'wwe2k16/matches.html'
	context_object_name = 'all_matches'

	def get_queryset(self):
		return Match.objects.order_by('event')

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
		if 'participants_list[]' in request_dict:
			participants_list = request_dict['participants_list[]']
		modified_participants_list = [str(x) for x in participants_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			try:
				match = form.save(commit=False)
				championship = match.championship
				belt_type = championship.belt_type
				old_champion = championship.champion.all()[0]
				match.winner = Wrestler.objects.get(name = request_dict['new_champion'][0])
				new_champion = match.winner
				match.championship.champion.set([new_champion])
				match.save()
				if old_champion.name != new_champion.name:
					if belt_type == 'PR':
						match.winner.primary += 1
					elif belt_type == 'SE':
						match.winner.secondary += 1
					elif belt_type == 'TE':
						match.winner.tertiary += 1
					elif belt_type == 'TT':
						match.winner.tag_team += 1
					match.winner.save()
					championship_history = ChampionshipHistory(match=match)
					championship_history.save()
					championship_history.old_champion.add(old_champion)
					championship_history.new_champion.add(new_champion)

				for x in modified_participants_list:
					participant = Wrestler.objects.get(name = x)
					match.participants.add(participant)

				data = {
					'result': 1,
					'message': 'Successfully added the match',
				}
			except Exception as e:
				data = {
					'result': 1,
					'message': e.message,
				}
		else: data = {
				'result': 0,
				'errors': json.loads(form.errors.as_json()),
			}
		return JsonResponse(data)

class MatchDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'pk' in kwargs:
			pk = kwargs['pk']
			Match.objects.get(pk=pk).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class MatchUpdate(UpdateView):
	model = Match
	fields = ['event', 'match_type', 'participants']
	template_name = 'wwe2k16/forms/update/match.html'

class TagTeamMatchCreate(View):
	form_class = TagMatchForm
	template_name = 'wwe2k16/forms/create/tag_team_match.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		request_dict = dict(request.POST.lists())
		print(request_dict)
		team1_list = request_dict['team1_list[]']
		team2_list = request_dict['team2_list[]']
		modified_team1_list = [str(x) for x in team1_list]
		modified_team2_list = [str(x) for x in team2_list]
		form = self.form_class(request.POST)
		if form.is_valid():
			try:
				match = form.save(commit=False)
				winner = match.tag_winner
				winning_team = []
				if winner == 't1':
					winning_team = modified_team1_list
				elif winner == 't2':
					winning_team = modified_team2_list
				old_champions = match.tag_championship.champion.all()
				old_champ_names = []
				for x in old_champions:
					old_champ_names.append(x.name)
				match.tag_championship.champion.clear()
				for x in winning_team:
					wrestler = Wrestler.objects.get(name = x)
					match.tag_championship.champion.add(wrestler)
				match.save()
				if (bool(set(old_champ_names).intersection(winning_team)) == False):
					championship_history = ChampionshipHistory(tag_match=match)
					championship_history.save()
					for x in old_champions:
						championship_history.old_champion.add(x)
					for x in winning_team:
						wrestler = Wrestler.objects.get(name = x)
						wrestler.tag_team += 1
						wrestler.save()
						championship_history.new_champion.add(x)
				for x in modified_team1_list:
					participant = Wrestler.objects.get(name = x)
					match.team1.add(participant)
				for x in modified_team2_list:
					participant = Wrestler.objects.get(name = x)
					match.team2.add(participant)
				
				data = {
					'result': 1,
					'message': 'Successfully added the tag team match',
				}
			except Exception as e:
				data = {
					'result': 1,
					'message': e.message,
				}
		else: data = {
				'result': 0,
				'errors': json.loads(form.errors.as_json()),
			}
		print(data)
		return JsonResponse(data)

class TagTeamMatchDelete(DeleteView):
	def post(self, request, *args, **kwargs):
		message = 'failed'
		if 'pk' in kwargs:
			pk = kwargs['pk']
			TagTeamMatch.objects.get(pk=pk).delete()
			message = 'deleted'
		return JsonResponse(message, safe=False)

class DraftHistoryCreate(View):
	def post(self, request):
		temp_draft = TemporaryDraft.objects.all()
		request_dict = dict(request.POST.lists())
		name = 'Draft New'
		message = ''
		try:
			if 'name' in request_dict:
				name = request_dict['name'][0]
			for draft in temp_draft:
				wrestler_list = []
				for wrestler in draft.wrestlers.all():
					wrestler_list.append(wrestler.name)
				new_draft = DraftHistory(
					name=name,
					brand = draft.brand,
					data=wrestler_list,
				)
				new_draft.save()
			message = 'Saved draft history'
		except Exception as e:
			data = {
				'result': 1,
				'message': e.message,
			}
		return JsonResponse(message, safe=False)

class DraftsView(View):
	template_name = 'wwe2k16/draft.html'

	def get(self, request):
		drafts = TemporaryDraft.objects.all()
		return render(request, self.template_name, {'drafts': drafts})

	def post(self, request):
		call_command('draft')
		return redirect('wwe2k16:drafts')

class DraftDelete(View):
	def post(self, request):
		deleted = TemporaryDraft.objects.all().delete()
		message = ''
		if deleted:
			message = 'deleted'
		else: message = 'failed'
		return JsonResponse(message, safe=False)

def get_wrestlers(request):
	mimetype = 'application/json'
	if request.is_ajax():
		q = request.GET.get('term', '')
		wrestlers = Wrestler.objects.filter(name__icontains = q)
		results = []
		for wrestler in wrestlers:
			results.append(wrestler.name)
	else:
		results = 'fail'
	return JsonResponse(results, safe=False)