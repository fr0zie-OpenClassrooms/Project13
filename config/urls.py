from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("account/", include("account.urls")),
    path("data/", include("dashboard.data.urls")),
    path("tracker/", include("dashboard.tracker.urls")),
    path("admin/", admin.site.urls),
]
