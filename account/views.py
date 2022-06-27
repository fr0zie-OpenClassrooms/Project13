from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    update_session_auth_hash,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegistrationForm, LoginForm, PasswordForm, PictureForm


class Login(View):
    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "account/login.html", context)

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data["remember_me"]
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("profile")
        messages.error(request, "Invalid username or password.")
        return redirect("login")


class Register(View):
    def get(self, request):
        form = RegistrationForm()
        context = {"form": form}
        return render(
            request,
            "account/register.html",
            context,
        )

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("profile")
        messages.error(request, "Unsuccessful registration. Invalid information.")


def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    password_form = PasswordForm(request.user)
    picture_form = PictureForm(request.user)
    context = {"password_form": password_form, "picture_form": picture_form}
    return render(request, "account/profile.html", context)


def change_password(request):
    form = PasswordForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password has been changed.")
    else:
        messages.error(request, "Invalid password.")
    return redirect("profile")


def change_picture(request):
    form = PictureForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        if request.FILES.get("picture", None) is not None:
            request.user.picture = request.FILES["picture"]
            request.user.save()
        messages.success(request, "Picture has been changed.")
    else:
        messages.error(request, "Unknown error.")
    return redirect("profile")


def recover_password(request):
    pass


def confirm_mail(request):
    pass
