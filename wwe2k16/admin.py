from django.contrib import admin
from .models import Brand, Wrestler, TagTeam, Event, Championship, MatchType, Match

models = [
    Brand, Wrestler, TagTeam, Event, Championship, MatchType, Match
]

for model in models:
    admin.site.register(model)