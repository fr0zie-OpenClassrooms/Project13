from django.urls import path
from . import views


urlpatterns = [
    path("", views.tracker, name="tracker"),
    path("connect-wallet", views.connect_wallet, name="connect-wallet"),
]
