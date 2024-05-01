from django.contrib import admin
from .models import Url, Match, Tournament, Participant


admin.site.register(Url)
admin.site.register(Match)
admin.site.register(Tournament)
admin.site.register(Participant)
