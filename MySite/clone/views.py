from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .models import User, Posts


# @login_required
def index(request):
    # if request.user.is_authenticated:
    #     return render(request, "clone/index.html", {})
    # return HttpResponseRedirect(reverse("login"))
    queueset = Posts.objects.filter(status=1).order_by("-created_on")
    return render(request, "clone/index2.html", {"post_list": queueset})

def PostDetails(request, slug):
    data = Posts.objects.filter(slug=slug).values('tittle', 'author', 'created_on', 'content')
    return render(request, "clone/post_detail.html", {"data": data})

class PostDetail(DetailView):
    model = Posts
    template_name = "clone/post_detail.html"


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "clone/login.html",
                {"message": "Invalid username and/or password.", "tipo": "danger"},
            )
    else:
        return render(request, "clone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "clone/register.html",
                {"message": "Passwords must match.", "tipo": "danger"},
            )
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "clone/register.html",
                {"message": "Username already taken.", "tipo": "danger"},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "clone/register.html")
