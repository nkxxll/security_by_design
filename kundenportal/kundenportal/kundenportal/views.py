from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as lo

from .utils.forms import CreateUserForm


def index(request):
    return render(request, "index.html", {})


def logout(request):
    lo(request)
    return HttpResponseRedirect("/", request)


def edit(request):
    return render(request, "edit.html")


def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # TODO:
            # crate user
            # log user in
            return HttpResponseRedirect("profile", request)
        else:
            # return form error
            return render(request, template_name="signup.html", context={"form": form})
    else:
        form = CreateUserForm()
    return render(request, template_name="signup.html", context={"form": form})


def profile(request):
    context = dict()
    return render(request, "profile.html", context)
