from django.urls import path
from . import views


urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("recover-password/", views.recover_password, name="recover-password"),
    path("confirm-mail/", views.confirm_mail, name="confirm-mail"),
]
