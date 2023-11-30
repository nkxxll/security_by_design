from django.urls import path

from . import views

appname = "signup"
urlpatterns = [
    path("", views.index, name="index"),
]
