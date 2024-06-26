from django.contrib import admin
from .models import Url, Match, Tournament, Participant
from preferences.admin import PreferencesAdmin
from .models import MyPreferences

admin.site.register(MyPreferences, PreferencesAdmin)


admin.site.register(Url)


class Participant_admin(admin.ModelAdmin):
    list_display = ("participant_id", "participant_name", "tournament_id")
    ordering = ("participant_id", "participant_name")


admin.site.register(Participant, Participant_admin)


class Match_admin(admin.ModelAdmin):
    list_display = (
        "match_id",
        "player1_id",
        "player2_id",
        "tournament_id",
        "suggested_play_order",
        "calculated_play_order",
        "match_state",
    )
    ordering = ("match_state", "calculated_play_order")


class Tournament_admin(admin.ModelAdmin):
    list_display = ("tournament_name", "tournament_id", "tournament_state")
    ordering = ("tournament_name",)


admin.site.register(Tournament, Tournament_admin)

admin.site.register(Match, Match_admin)
