from json import loads
from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as lo
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from power_data.models import PowerData
import requests

from .utils.forms import CreateUserForm, CreateUserMeta

class Period():
    YEAR = "year"
    MONTH = "month"

# TODO not sure if this is the right url
MSB_API_URL = "http://localhost:8000/stromdaten"


def index(request):
    return render(request, "index.html", {})


def logout(request):
    lo(request)
    return HttpResponseRedirect("/", request)

@login_required
def edit(request):
    return render(request, "edit.html")


def signup(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        data_form = CreateUserMeta(request.POST)
        if user_form.is_valid() and data_form.is_valid():
            # TODO:
            # crate user
            # log user in
            return HttpResponseRedirect("profile", request)
        else:
            # return form error
            return render(
                request, template_name="signup.html", context={"user_form": user_form, "data_form": data_form}
            )
    else:
        user_form = CreateUserForm()
        data_form = CreateUserMeta()
    return render(
        request, template_name="signup.html", context={"user_form": user_form, "data_form": data_form}
    )


@login_required
def profile(request):
    context = dict()
    context["power_data"] = _get_powerdata(request.user, Period.YEAR)
    return render(request, "profile.html", context)

def _get_powerdata(user: User, period: str, year: int = datetime.now().year, month: int = datetime.now().month) -> dict:
    """get all user power data for a specific user and time period

    Gets all power data for a user for a specific period. The period can be a year or a month.
    The data is fetched from the msb api and returned as a dict.

    TODO: what format should the data be in?
    TODO: how should i handle the time period specifications for the power data
    which options should be there?

    Args:
        user (User): user to get data for
        period (Period): period to get data for
        year (int, optional): year to get data for. Defaults to datetime.now().year.
        month (int, optional): month to get data for. Defaults to datetime.now().month.
    Returns:
        dict: list of power data for user
    """
    session = requests.Session()
    cookies = {
            "key": PowerData.objects.get(user=user).auth_key
            }
    session.cookies.update(cookies)
    # TODO finish this url part with period and year and month
    response = session.get(f"MSB_API_URL/{year}/{month}")
    # TODO check if the json data needs to be cleaned up
    # TODO validate the json data
    return loads(response.json())
