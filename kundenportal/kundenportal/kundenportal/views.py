from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as lo


def index(request):
    return render(request, template_name="templates/kundenportal/index.html")


def logout(request):
    lo(request)
    return HttpResponseRedirect("/", request)


def login(request):
    pass


def edit(request):
    pass


def signup(request):
    pass


def profile(request):
    pass
