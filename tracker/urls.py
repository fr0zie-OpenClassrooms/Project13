from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path("", login_required(views.Holdings.as_view()), name="tracker"),
    path(
        "connect-wallet",
        login_required(views.ConnectWallet.as_view()),
        name="connect-wallet",
    ),
    path("holdings", login_required(views.Holdings.as_view()), name="view-holdings"),
    path(
        "transactions",
        login_required(views.Transactions.as_view()),
        name="view-transactions",
    ),
]
