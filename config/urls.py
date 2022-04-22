from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("account/", include("account.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
]
