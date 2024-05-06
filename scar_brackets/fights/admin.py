from django.contrib import admin
from .models import Url, Match, Tournament, Participant


admin.site.register(Url)
admin.site.register(Match)
admin.site.register(Tournament)


class Participant_admin(admin.ModelAdmin):
    list_display = ("participant_id", "participant_name")
    ordering = ("participant_id", "participant_name")


admin.site.register(Participant, Participant_admin)
