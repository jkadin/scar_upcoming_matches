from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("challonge", views.challonge_index, name="challonge_index"),
    path("display_matches", views.display_matches, name="display_matches"),
    path("stream", views.no_background_index, name="stream"),
    path("reorder", views.manual_sort, name="reorder"),
    path("time_remaining", views.time_remaining, name="time_remaining"),
    path(
        "time_remaining_inner", views.time_remaining_inner, name="time_remaining_inner"
    ),
    path("bot/<str:participant_name>/", views.bot, name="bot"),
    path("time_out", views.time_out, name="time_out"),
    path(
        "claim_bot/<str:participant_name>/",
        views.claim_bot,
        name="claim_bot",
    ),
    path("user/<int:user_id>/", views.user, name="user"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
