from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("login", views.signIn, name="login"),
  path("register", views.register, name="register"),
  path("logout", views.signout, name="logout"),
  path("newPost", views.newPost, name="newPost"),
  path("posting/<int:id>", views.posting, name="posting")
]