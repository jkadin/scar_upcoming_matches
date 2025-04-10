from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("challonge", views.challonge_index, name="challonge_index"),
    path("display_matches", views.display_matches, name="display_matches"),
    path("stream", views.no_background_index, name="stream"),
    path("manual_sort", views.manual_sort, name="manual_sort"),
    path("time_remaining", views.time_remaining, name="time_remaining"),
    path(
        "time_remaining_inner",
        views.time_remaining_inner,
        name="time_remaining_inner",
    ),
    path("bot/<str:bot_name>/", views.bot, name="bot"),
    path(
        "time_remaining_bot/<str:bot_name>/",
        views.time_remaining_bot,
        name="time_remaining_bot",
    ),
    path("time_out", views.time_out, name="time_out"),
    path(
        "claim_bot/<str:bot_name>/",
        views.claim_bot,
        name="claim_bot",
    ),
    path(
        "claim_multiple_bots/",
        views.claim_multiple_bots,  # type: ignore
        name="claim_multiple_bots",
    ),  # type: ignore
    path("create_user/", views.create_user, name="create_user"),  # type: ignore
    path("user/<int:user_id>/", views.user, name="user"),
]

# Add debug toolbar URLs
urlpatterns += debug_toolbar_urls()

# Add static file serving during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
