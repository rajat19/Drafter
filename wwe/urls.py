from django.conf.urls import url
from . import views

app_name = 'wwe'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),

    # /wwe/brands
    url(r'^brands/$', views.BrandsView.as_view(), name='brands'),

    # /wwe/brand/raw
    url(r'^brand/(?P<slug>[\w-]+)$', views.BrandView.as_view(), name='brand'),

    # /wwe/brand/add
    url(r'^brand/add/$', views.BrandCreate.as_view(), name='brand-add'),

    # /wwe/brand/raw/update
    url(r'^brand/(?P<slug>[\w-]+)/update/$', views.BrandUpdate.as_view(), name='brand-update'),

    # /wwe/brand/raw/delete
    url(r'^brand/(?P<slug>[\w-]+)/delete/$', views.BrandDelete.as_view(), name='brand-delete'),

    # /wwe/wrestlers
    url(r'^wrestlers/$', views.WrestlersView.as_view(), name='wrestlers'),

    # /wwe/wrestler/undertaker
    url(r'^wrestler/(?P<slug>[\w-]+)$', views.WrestlerView.as_view(), name='wrestler'),

    # /wwe/wrestler/add
    url(r'^wrestler/add/$', views.WrestlerCreate.as_view(), name='wrestler-add'),

    # /wwe/wrestler/undertaker/update
    url(r'^wrestler/(?P<slug>[\w-]+)/update/$', views.WrestlerUpdate.as_view(), name='wrestler-update'),

    # /wwe/wrestler/undertaker/delete
    url(r'^wrestler/(?P<slug>[\w-]+)/delete/$', views.WrestlerDelete.as_view(), name='wrestler-delete'),

    # /wwe/tagteams
    url(r'^tagteams/$', views.TagTeamsView.as_view(), name='tagteams'),

    # /wwe/tagteam/nwo
    url(r'^tagteam/(?P<slug>[\w-]+)$', views.TagTeamView.as_view(), name='tagteam'),

    # /wwe/tagteam/add
    url(r'^tagteam/add/$', views.TagTeamCreate.as_view(), name='tagteam-add'),

    # /wwe/tagteam/nwo/update
    url(r'^tagteam/(?P<slug>[\w-]+)/update/$', views.TagTeamUpdate.as_view(), name='tagteam-update'),

    # /wwe/tagteam/nwo/delete
    url(r'^tagteam/(?P<slug>[\w-]+)/delete/$', views.TagTeamDelete.as_view(), name='tagteam-delete'),

    # /wwe/championships
    url(r'^championships/$', views.ChampionshipsView.as_view(), name='championships'),

    # /wwe/championship/templates.wwe
    url(r'^championship/(?P<slug>[\w-]+)$', views.ChampionshipView.as_view(), name='championship'),

    # /wwe/championship/add
    url(r'^championship/add/$', views.ChampionshipCreate.as_view(), name='championship-add'),

    # /wwe/championship/templates.wwe/update
    url(r'^championship/(?P<slug>[\w-]+)/update/$', views.ChampionshipUpdate.as_view(), name='championship-update'),

    # /wwe/championship/templates.wwe/delete
    url(r'^championship/(?P<slug>[\w-]+)/delete/$', views.ChampionshipDelete.as_view(), name='championship-delete'),

    # /wwe/events
    url(r'^events/$', views.EventsView.as_view(), name='events'),

    # /wwe/event/wrestlemania
    url(r'^event/(?P<slug>[\w-]+)$', views.EventView.as_view(), name='event'),

    # /wwe/event/add
    url(r'^event/add/$', views.EventCreate.as_view(), name='event-add'),

    # /wwe/event/wrestlemania/update
    url(r'^event/(?P<slug>[\w-]+)/update/$', views.EventUpdate.as_view(), name='event-update'),

    # /wwe/event/wrestlemania/delete
    url(r'^event/(?P<slug>[\w-]+)/delete/$', views.EventDelete.as_view(), name='event-delete'),

    # /wwe/matchtypes
    url(r'^matchtypes/$', views.MatchTypesView.as_view(), name='matchtypes'),

    # /wwe/matchtype/triple-threat
    url(r'^matchtype/(?P<slug>[\w-]+)$', views.MatchTypeView.as_view(), name='matchtype'),

    # /wwe/matchtype/add
    url(r'^matchtype/add/$', views.MatchTypeCreate.as_view(), name='matchtype-add'),

    # /wwe/matchtype/triple-threat/update
    url(r'^matchtype/(?P<slug>[\w-]+)/update/$', views.MatchTypeUpdate.as_view(), name='matchtype-update'),

    # /wwe/matchtype/triple-threat/delete
    url(r'^matchtype/(?P<slug>[\w-]+)/delete/$', views.MatchTypeDelete.as_view(), name='matchtype-delete'),

    # /wwe/match/add
    url(r'^match/add/$', views.MatchCreate.as_view(), name='match-add'),

    # /wwe/match/1/delete
    url(r'^match/(?P<pk>[0-9]+)/delete/$', views.MatchDelete.as_view(), name='tagmatch-delete'),

    # /wwe/match/tagteam/add
    url(r'^tagmatch/add/$', views.TagTeamMatchCreate.as_view(), name='tagmatch-add'),

    # /wwe/tagmatch/1/delete
    url(r'^tagmatch/(?P<pk>[0-9]+)/delete/$', views.TagTeamMatchDelete.as_view(), name='tagmatch-delete'),

    # /wwe/drafts
    url(r'^drafts/', views.DraftsView.as_view(), name='drafts'),

    # /wwe/drafthistory/save
    url(r'^drafthistory/create/$', views.DraftHistoryCreate.as_view(), name='drafthistory-add'),

    # /wwe/draft/delete
    url(r'^draft/delete/$', views.DraftDelete.as_view(), name='draft-delete'),

    # /wwe/ajax/wrestlers
    url(r'^api/wrestlers/$', views.get_wrestlers, name='wrestlers-api'),
]
