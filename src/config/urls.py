# src/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(_request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", health),                 # optional: makes / return 200
    path("health/", health),          # recommended: /health/
    path("admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
]
