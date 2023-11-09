from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def show_profile(request):
    if request.user.is_authenticated:
        return render(request, "accounts/profile.html")
    else:
        return HttpResponseRedirect(request, 'login')
