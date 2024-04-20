from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("fights/", include("fights.urls")),
    path("admin/", admin.site.urls),
]
