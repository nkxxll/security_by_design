from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout


def index(request):
    return render(request, template_name='kundenportal/index.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/', request)
