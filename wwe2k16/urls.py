from django.conf.urls import url
from . import views

app_name = 'wwe2k16'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='brands'),

    # /wwe2k16/brand/raw
    url(r'^brand/(?P<slug>[\w-]+)$', views.BrandView.as_view(), name='brand'),

    # /wwe2k16/brand/add
    url(r'^brand/add/$', views.BrandCreate.as_view(), name='brand-add'),

    # /wwe2k16/brand/raw/update
    url(r'^brand/(?P<slug>[\w-]+)/update/$', views.BrandUpdate.as_view(), name='brand-update'),

    # /wwe2k16/brand/raw/delete
    url(r'^brand/(?P<slug>[\w-]+)/delete/$', views.BrandDelete.as_view(), name='brand-delete'),
    
    # /wwe2k16/wrestlers
    url(r'^wrestlers/$', views.WrestlersView.as_view(), name='wrestlers'),

    # /wwe2k16/wrestler/undertaker
    url(r'^wrestler/(?P<slug>[\w-]+)$', views.WrestlerView.as_view(), name='wrestler'),

    # /wwe2k16/wrestler/add
    url(r'^wrestler/add/$', views.WrestlerCreate.as_view(), name='wrestler-add'),

    # /wwe2k16/wrestler/undertaker/update
    url(r'^wrestler/(?P<slug>[\w-]+)/update/$', views.WrestlerUpdate.as_view(), name='wrestler-update'),

    # /wwe2k16/wrestler/undertaker/delete
    url(r'^wrestler/(?P<slug>[\w-]+)/delete/$', views.WrestlerDelete.as_view(), name='wrestler-delete'),

    # /wwe2k16/tagteams
    url(r'^tagteams/$', views.TagTeamsView.as_view(), name='tagteams'),

    # /wwe2k16/tagteam/nwo
    url(r'^tagteam/(?P<slug>[\w-]+)$', views.TagTeamView.as_view(), name='tagteam'),

    # /wwe2k16/tagteam/add
    url(r'^tagteam/add/$', views.TagTeamCreate.as_view(), name='tagteam-add'),

    # /wwe2k16/tagteam/nwo/update
    url(r'^tagteam/(?P<slug>[\w-]+)/update/$', views.TagTeamUpdate.as_view(), name='tagteam-update'),

    # /wwe2k16/tagteam/nwo/delete
    url(r'^tagteam/(?P<slug>[\w-]+)/delete/$', views.TagTeamDelete.as_view(), name='tagteam-delete'),

    # /wwe2k16/championships
    url(r'^championships/$', views.ChampionshipsView.as_view(), name='championships'),

    # /wwe2k16/championship/wwe
    url(r'^championship/(?P<slug>[\w-]+)$', views.ChampionshipView.as_view(), name='championship'),

    # /wwe2k16/championship/add
    url(r'^championship/add/$', views.ChampionshipCreate.as_view(), name='championship-add'),

    # /wwe2k16/championship/wwe/update
    url(r'^championship/(?P<slug>[\w-]+)/update/$', views.ChampionshipUpdate.as_view(), name='championship-update'),

    # /wwe2k16/championship/wwe/delete
    url(r'^championship/(?P<slug>[\w-]+)/delete/$', views.ChampionshipDelete.as_view(), name='championship-delete'),

    # /wwe2k16/events
    url(r'^events/$', views.EventsView.as_view(), name='events'),

    # /wwe2k16/event/wrestlemania
    url(r'^event/(?P<slug>[\w-]+)$', views.EventView.as_view(), name='event'),

    # /wwe2k16/event/add
    url(r'^event/add/$', views.EventCreate.as_view(), name='event-add'),

    # /wwe2k16/event/wrestlemania/update
    url(r'^event/(?P<slug>[\w-]+)/update/$', views.EventUpdate.as_view(), name='event-update'),

    # /wwe2k16/event/wrestlemania/delete
    url(r'^event/(?P<slug>[\w-]+)/delete/$', views.EventDelete.as_view(), name='event-delete'),

    # /wwe2k16/matchtypes
    url(r'^matchtypes/$', views.MatchTypesView.as_view(), name='matchtypes'),

    # /wwe2k16/matchtype/triple-threat
    url(r'^matchtype/(?P<slug>[\w-]+)$', views.MatchTypeView.as_view(), name='matchtype'),

    # /wwe2k16/matchtype/add
    url(r'^matchtype/add/$', views.MatchTypeCreate.as_view(), name='matchtype-add'),

    # /wwe2k16/matchtype/triple-threat/update
    url(r'^matchtype/(?P<slug>[\w-]+)/update/$', views.MatchTypeUpdate.as_view(), name='matchtype-update'),

    # /wwe2k16/matchtype/triple-threat/delete
    url(r'^matchtype/(?P<slug>[\w-]+)/delete/$', views.MatchTypeDelete.as_view(), name='matchtype-delete'),

    # /wwe2k16/match/add
    url(r'^match/add/$', views.MatchCreate.as_view(), name='match-add'),

]