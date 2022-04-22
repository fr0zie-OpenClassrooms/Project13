from django.urls import path, include


urlpatterns = [
    path("tracker/", include("dashboard.tracker.urls")),
    path("data/", include("dashboard.data.urls")),
]
