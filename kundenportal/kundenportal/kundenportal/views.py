from json import loads
from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as lo
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from power_data.models import PowerData
import requests

from .utils.forms import CreateUserForm, CreateUserMeta, CreateEditData


class Period:
    YEAR = "year"
    MONTH = "month"


# TODO not sure if this is the right url
MSB_API_URL = "http://localhost:8000/stromdaten"


def index(request):
    return render(request, "index.html", {})


def logout(request):
    lo(request)
    return HttpResponseRedirect("/", request)


@login_required(login_url="/login")
def edit(request):
    initial = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "street": PowerData.objects.get(user=request.user).street,
        "street_number": PowerData.objects.get(user=request.user).street_number,
        "postal_code": PowerData.objects.get(user=request.user).postal_code,
        "city": PowerData.objects.get(user=request.user).city,
    }
    if request.method == "POST":
        edit_data_form = CreateEditData(request.POST, initial=initial)
        if edit_data_form.is_valid():
            # update user data
            request.user.first_name = edit_data_form.cleaned_data["first_name"]
            request.user.last_name = edit_data_form.cleaned_data["last_name"]
            request.user.email = edit_data_form.cleaned_data["email"]
            # update meta data
            power_data = PowerData.objects.get(user=request.user)
            power_data.street = edit_data_form.cleaned_data["street"]
            power_data.street_number = edit_data_form.cleaned_data["street_number"]
            power_data.postal_code = edit_data_form.cleaned_data["postal_code"]
            power_data.city = edit_data_form.cleaned_data["city"]
            request.user.save()
            power_data.save()
            # update user data
            return HttpResponseRedirect("/profile", request)
        else:
            # return form error
            return render(
                request,
                template_name="edit.html",
                context={"edit_data_form": edit_data_form},
            )
    else:
        edit_data_form = CreateEditData(request.POST or None, initial=initial)
    return render(
        request, template_name="edit.html", context={"edit_data_form": edit_data_form}
    )


def signup(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        data_form = CreateUserMeta(request.POST)
        if user_form.is_valid() and data_form.is_valid():
            # TODO:
            # create user
            user = User.objects.create_user(
                user_form.cleaned_data["username"],
                user_form.cleaned_data["email"],
                user_form.cleaned_data["password"],
            )
            user.last_name = user_form.cleaned_data["last_name"]
            user.first_name = user_form.cleaned_data["first_name"]
            user.save()
            # log user in
            pd = PowerData.objects.create(
                user=user,
                contract=data_form.cleaned_data["contract"],
                auth_key=data_form.cleaned_data["auth_key"],
                street=data_form.cleaned_data["street"],
                street_number=data_form.cleaned_data["street_number"],
                postal_code=data_form.cleaned_data["postal_code"],
                city=data_form.cleaned_data["city"],
            )
            # when we have the new user created and all the data set up we want to log this user in
            request.user = user
            lo(request)
            return HttpResponseRedirect("/profile", request)
        else:
            # return form error
            return render(
                request,
                template_name="signup.html",
                context={"user_form": user_form, "data_form": data_form},
            )
    else:
        user_form = CreateUserForm()
        data_form = CreateUserMeta()
    return render(
        request,
        template_name="signup.html",
        context={"user_form": user_form, "data_form": data_form},
    )


@login_required(login_url="/login")
def profile(request):
    context = dict()
    context["power_data"] = _get_powerdata(request.user, Period.YEAR)
    return render(request, "profile.html", context)


def _get_powerdata(
    user: User,
    period: str,
    year: int = datetime.now().year,
    month: int = datetime.now().month,
) -> dict:
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
    cookies = {"key": PowerData.objects.get(user=user).auth_key}
    session.cookies.update(cookies)
    # TODO finish this url part with period and year and month
    response = session.get(f"MSB_API_URL/{year}/{month}")
    # TODO check if the json data needs to be cleaned up
    # TODO validate the json data
    return loads(response.json())
