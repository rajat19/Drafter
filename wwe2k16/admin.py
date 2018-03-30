from django.contrib import admin
from .models import Brand, Wrestler, TagTeam, Event, Championship, MatchType, Match, TagTeamMatch, ChampionshipHistory, DraftHistory, TemporaryDraft

models = [
    Brand, Wrestler, TagTeam, Event, Championship, MatchType, Match, TagTeamMatch, ChampionshipHistory, DraftHistory, TemporaryDraft
]

for model in models:
    admin.site.register(model)