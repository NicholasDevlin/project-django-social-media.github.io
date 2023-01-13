from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Posting, References
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

# Create your views here.

def index(request):
  if request.method == "GET":
      search = request.GET.get('search')
      if search:
        allPost = Posting.objects.filter(Q(title__icontains=search))
        return render(request, "wordle/index.html", {
          "allPosting": allPost
        })
      else:
        allPost = Posting.objects.all()
        return render(request, "wordle/index.html", {
            "allPosting": allPost
        })
  else:
      allPost = Posting.objects.all()
      return render(request, "wordle/index.html", {
            "allPosting": allPost
      })


def posting(request, id):
  postingData = Posting.objects.get(pk=id)
  writer = request.user.username == postingData.writer.username
  return render(request, "wordle/posting.html", {
    "posting": postingData,
    "writer": writer
  })


def newPost(request):
  if request.method == "POST":
    title = request.POST["title"]
    reference = request.POST["reference"]
    status = request.POST["status"]
    writer = request.user
    referencesData = References.objects.get(referenceFrom=reference)

    newPosting = Posting(
      title = title,
      reference = referencesData,
      words = status,
      writer = writer
    )
    newPosting.save()
    return HttpResponseRedirect(reverse("index"))
  else:
    return render(request, "wordle/newPost.html")

def signIn(request):
  if request.method == "POST":
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
      else:
        return render(request, "wordle/login.html", {
          "message": "invalid email and/or password"
        })

  else:
      return render(request, "wordle/login.html")

def signout(request):
  logout(request)
  return HttpResponseRedirect(reverse("index"))

def register(request):
  if request.method == "POST":
    username = request.POST["username"]
    email = request.POST["email"]

    # confirmation password
    password = request.POST["password"]
    confirmPassword = request.POST["confirmPassword"]
    if password != confirmPassword:
      return render(request, "wordle/register.html", {
        "message": "Password must match."
      })

    try:
      user = User.objects.create_user(username, email, password)
      user.save()
    except IntegrityError:
      return render(request, "wordle/register.html", {
        "message": "Username is already taken."
      })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
    
  else:
    return render(request, "wordle/register.html")
