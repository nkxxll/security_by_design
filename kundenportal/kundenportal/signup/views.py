from django.shortcuts import render
from django.views.generic.base import HttpResponseRedirect
from .extras.forms import CreateUserForm

# Create your views here.


def index(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # TODO:
            # crate user
            # log user in
            return HttpResponseRedirect("/accouts/profile", request)
        else:
            # return form error
            return render(
                request, template_name="signup/create_user.html", context={"form": form}
            )
    else:
        form = CreateUserForm()
    return render(
        request, template_name="signup/create_user.html", context={"form": form}
    )
