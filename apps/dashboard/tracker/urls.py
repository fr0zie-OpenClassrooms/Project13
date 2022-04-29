from django.urls import path
from . import views


urlpatterns = [
    path("", views.Tracker.as_view(), name="tracker"),
    path("connect-wallet", views.ConnectWallet.as_view(), name="connect-wallet"),
    path("holdings", views.Balance.as_view(), name="view-holdings"),
]
