from django.contrib import admin
from .models import Url, Match, Tournament, Participant


admin.site.register(Url)
admin.site.register(Tournament)


class Participant_admin(admin.ModelAdmin):
    list_display = ("participant_id", "participant_name", "tournament_id")
    ordering = ("participant_id", "participant_name")


admin.site.register(Participant, Participant_admin)


class Match_admin(admin.ModelAdmin):
    list_display = ("match_id", "player1_id", "player2_id", "tournament_id")
    ordering = ("match_id", "player1_id")


admin.site.register(Match, Match_admin)
