from django.core.management import call_command
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_countries.widgets import CountrySelectWidget
import json

from .models import Brand, Wrestler, Championship, Event, Match, TagTeamMatch, MatchType, TagTeam, ChampionshipHistory, DraftHistory, TemporaryDraft
from .forms import MatchForm, ChampionshipForm, TagTeamForm, TagMatchForm


class StaticTemplates:
    version = 'wwe'
    create = '{}/forms/create/{}.html'
    view = '{}/{}.html'
    update = '{}/forms/update/{}.html'

    def get_create_template_name(self, link):
        return self.create.format(self.version, link)

    def get_view_template_name(self, link):
        return self.view.format(self.version, link)

    def get_update_template_name(self, link):
        return self.update.format(self.version, link)


static_templates = StaticTemplates()


class IndexView(TemplateView):
    template_name = static_templates.get_view_template_name('index')


class BrandsView(generic.ListView):
    template_name = static_templates.get_view_template_name('brands')
    context_object_name = 'all_brands'

    def get_queryset(self):
        return Brand.objects.order_by('created_at')


class BrandView(generic.DetailView):
    model = Brand
    template_name = static_templates.get_view_template_name('brand')


class BrandCreate(CreateView):
    model = Brand
    fields = Brand.db_fields()
    template_name = static_templates.get_create_template_name('brand')


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
    fields = Brand.db_fields()
    template_name = static_templates.get_create_template_name('brand')


class WrestlersView(generic.ListView):
    template_name = static_templates.get_view_template_name('wrestlers')
    context_object_name = 'all_wrestlers'

    def get_queryset(self):
        return Wrestler.objects.order_by('name')


class WrestlerView(generic.DetailView):
    model = Wrestler
    template_name = static_templates.get_view_template_name('wrestler')


class WrestlerCreate(CreateView):
    model = Wrestler
    fields = Wrestler.db_fields()
    widgets = {'country': CountrySelectWidget()}
    template_name = static_templates.get_create_template_name('wrestler')


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
    fields = Wrestler.db_fields()
    widgets = {'country': CountrySelectWidget()}
    template_name = static_templates.get_update_template_name('wrestler')


class TagTeamsView(generic.ListView):
    template_name = static_templates.get_view_template_name('tag_teams')
    context_object_name = 'all_tag_teams'

    def get_queryset(self):
        return TagTeam.objects.order_by('name')


class TagTeamView(generic.DetailView):
    model = TagTeam
    template_name = static_templates.get_view_template_name('tag_team')


class TagTeamCreate(CreateView):
    form_class = TagTeamForm
    template_name = static_templates.get_create_template_name('tag_team')

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
        else:
            data = {
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
    template_name = static_templates.get_update_template_name('tag_team')


class EventsView(generic.ListView):
    template_name = static_templates.get_view_template_name('events')
    context_object_name = 'all_events'

    def get_queryset(self):
        return Event.objects.order_by('created_at')


class EventView(View):
    model = Event
    template_name = static_templates.get_view_template_name('event')
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
    fields = Event.db_fields()
    template_name = static_templates.get_create_template_name('event')


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
    fields = Event.db_fields()
    template_name = static_templates.get_update_template_name('event')


class ChampionshipsView(generic.ListView):
    template_name = static_templates.get_view_template_name('championships')
    context_object_name = 'all_championships'

    def get_queryset(self):
        return Championship.objects.order_by('created_at')


class ChampionshipView(generic.DetailView):
    model = Championship
    template_name = static_templates.get_view_template_name('championship')


class ChampionshipCreate(CreateView):
    form_class = ChampionshipForm
    template_name = static_templates.get_create_template_name('championship')

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
                    'message': str(e),
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
                message = str(e)
        return JsonResponse(message, safe=False)


class ChampionshipUpdate(UpdateView):
    model = Championship
    fields = ['name', 'belt_type', 'champion']
    template_name = static_templates.get_update_template_name('championship')


class MatchTypesView(generic.ListView):
    template_name = static_templates.get_view_template_name('match_types')
    context_object_name = 'all_match_types'

    def get_queryset(self):
        return MatchType.objects.order_by('name')


class MatchTypeView(generic.DetailView):
    model = MatchType
    template_name = static_templates.get_view_template_name('match_type')


class MatchTypeCreate(CreateView):
    model = MatchType
    fields = ['name', 'no_of_participants']
    template_name = static_templates.get_create_template_name('match_type')


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
    template_name = static_templates.get_update_template_name('match_type')


class MatchesView(generic.ListView):
    template_name = static_templates.get_view_template_name('matches')
    context_object_name = 'all_matches'

    def get_queryset(self):
        return Match.objects.order_by('event')


class MatchView(generic.DetailView):
    model = Match
    template_name = static_templates.get_view_template_name('match')


class MatchCreate(View):
    form_class = MatchForm
    template_name = static_templates.get_create_template_name('match')

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
                if belt_type == 'PR':
                    match.winner.primary += 1
                elif belt_type == 'SE':
                    match.winner.secondary += 1
                elif belt_type == 'TE':
                    match.winner.tertiary += 1
                elif belt_type == 'TT':
                    match.winner.tag_team += 1
                match.winner.save()
                if old_champion.name != new_champion.name:
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
    template_name = static_templates.get_update_template_name('match')


class TagTeamMatchCreate(View):
    form_class = TagMatchForm
    template_name = static_templates.get_create_template_name('tag_team_match')

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        request_dict = dict(request.POST.lists())
        team1_list = request_dict['team1_list[]']
        team2_list = request_dict['team2_list[]']
        modified_team1_list = [str(x) for x in team1_list]
        modified_team2_list = [str(x) for x in team2_list]
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                match = form.save(commit=False)
                winner = match.tag_winner
                winning_team = modified_team1_list if winner == 't1' else modified_team2_list
                old_champions = match.tag_championship.champion.all()
                old_champ_names = [x.name for x in old_champions]
                match.tag_championship.champion.clear()
                for x in winning_team:
                    wrestler = Wrestler.objects.get(name=x)
                    wrestler.tag_team += 1
                    wrestler.save()
                    match.tag_championship.champion.add(wrestler)
                match.save()

                # winning team is not the old champions
                if len(set(old_champ_names).intersection(winning_team)) == 0:
                    championship_history = ChampionshipHistory(tag_match=match)
                    championship_history.save()
                    for x in old_champions:
                        championship_history.old_champion.add(x)
                    for x in winning_team:
                        wrestler = Wrestler.objects.get(name=x)
                        championship_history.new_champion.add(wrestler)
                for x in modified_team1_list:
                    participant = Wrestler.objects.get(name=x)
                    match.team1.add(participant)
                for x in modified_team2_list:
                    participant = Wrestler.objects.get(name=x)
                    match.team2.add(participant)

                data = {
                    'result': 1,
                    'message': 'Successfully added the tag team match',
                }
            except Exception as e:
                data = {
                    'result': 1,
                    'message': str(e),
                }
        else:
            data = {
                'result': 0,
                'errors': json.loads(form.errors.as_json()),
            }
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
        try:
            if 'name' in request_dict:
                name = request_dict['name'][0]
            for draft in temp_draft:
                wrestler_list = []
                for wrestler in draft.wrestlers.all():
                    wrestler_list.append(wrestler.name)
                    wrestler.brand = draft.brand
                    wrestler.save()
                new_draft = DraftHistory(
                    name=name,
                    brand=draft.brand,
                    data=wrestler_list,
                )
                new_draft.save()
            message = 'Saved draft history'
        except Exception as e:
            message = str(e)
        data = {
            'result': 1,
            'message': message,
        }
        return JsonResponse(data, safe=False)


class DraftsView(View):
    template_name = static_templates.get_view_template_name('draft')

    def get(self, request):
        drafts = TemporaryDraft.objects.all()
        return render(request, self.template_name, {'drafts': drafts})

    def post(self, request):
        call_command('draft')
        return redirect('wwe:drafts')


class DraftDelete(View):
    def post(self, request):
        deleted = TemporaryDraft.objects.all().delete()
        if deleted:
            message = 'deleted'
        else:
            message = 'failed'
        return JsonResponse(message, safe=False)


def get_wrestlers(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        wrestlers = Wrestler.objects.filter(name__icontains = q)
        results = []
        for wrestler in wrestlers:
            results.append(wrestler.name)
    else:
        results = 'fail'
    return JsonResponse(results, safe=False)
