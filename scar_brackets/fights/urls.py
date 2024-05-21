from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("display_matches", views.display_matches, name="display_matches"),
    path("stream", views.no_background_index, name="stream"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
