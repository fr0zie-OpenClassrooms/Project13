from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("account/", include("account.urls")),
    path("dashboard/data/", include("data.urls")),
    path("dashboard/tracker/", include("tracker.urls")),
    path("admin/", admin.site.urls),
]
