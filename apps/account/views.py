from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegistrationForm, LoginForm


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
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("tracker")
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
            return redirect("tracker")
        messages.error(request, "Unsuccessful registration. Invalid information.")


def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    return render(request, "account/profile.html")


def recover_password(request):
    pass


def confirm_mail(request):
    pass
