from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/fights/")),
    path("fights/", include("fights.urls")),
    path("admin/", admin.site.urls),
    path("accounts/login/", RedirectView.as_view(url="/accounts/discord/login/")),
    path("accounts/", include("allauth.urls")),
]
