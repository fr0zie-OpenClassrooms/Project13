from django.contrib import messages
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import UserForm


@login_required(login_url="login")
def profile(request):
    return render(request, "account/profile.html")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("tracker")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "account/login.html", context)


def logout(request):
    auth_logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("tracker")


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("tracker")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserForm()
    context = {"form": form}
    return render(
        request,
        "account/register.html",
        context,
    )


def recover_password(request):
    pass


def confirm_mail(request):
    pass
