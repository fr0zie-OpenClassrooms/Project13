from django.urls import path
from . import views


urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.Register.as_view(), name="register"),
    path("change-picture", views.change_picture, name="change-picture"),
    path("change-password", views.change_password, name="change-password"),
    path("recover-password", views.recover_password, name="recover-password"),
    path("confirm-mail", views.confirm_mail, name="confirm-mail"),
]
