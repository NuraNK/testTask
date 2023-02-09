from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token

from .forms import LoginForm
from .models import User


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            if "@" in username:
                user = authenticate(email=username, password=password)
            else:
                user = authenticate(phone=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_view")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "login.html", {"form": form, "msg": msg})


@login_required
def home_view(request):
    return render(request, "home.html", {"user": request.user})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login_view")
