from typing import Tuple
from logging import getLogger
from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as lo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from power_data.models import PowerData

# this is for the power data validation
import requests

from .utils.forms import CreateUserForm, CreateUserMeta, CreateEditData

LOGGER = getLogger(__name__)

MSB_PORT = 3000
MSB_HOST = "localhost"
MSB_API_ROUTE = "api/v1/stromverbrauch"
MSB_API_URL = f"http://{MSB_HOST}:{MSB_PORT}/{MSB_API_ROUTE}"


def index(request):
    return render(request, "index.html", {})


def logout(request):
    lo(request)
    return render(request, "logout.html", {})


def notfound(request):
    return render(request, "404.html", {})


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
    power_data = dict()
    power_data["stromverbrauch"] = _get_powerdata(request.user, ("", ""))
    power_data["stromverbrauch_23"] = _get_powerdata(request.user, ("", ""), year=2023)
    power_data["stromverbrauch_q423"] = _get_powerdata(request.user, ("2023-10-01", "2023-12-31"))
    context["power_data"] = power_data
    LOGGER.debug(context["power_data"])
    return render(request, "profile.html", context)


def _get_powerdata(
    user: User,
    period: Tuple[str, str],
    year: int | None = None,
) -> dict:
    """get all user power data for a specific user and time period

    Gets all power data for a user for a specific period. The period can be a year or a month.
    The data is fetched from the msb api and returned as a dict.

    Args:
        user (User): user to get data for
        period (Tuple[str, str]): period to get data for
        year (int, optional): year to get data for. Defaults to datetime.now().year.
    Returns:
        dict: list of power data for user, the dict is empty if there is no data or an error occurred
    """
    data = dict()  # data that is returned
    # requests session
    session = requests.Session()
    cookies = {"auth_key": PowerData.objects.get(user=user).auth_key}
    session.cookies.update(cookies)

    # build request URL
    request_url_str = MSB_API_URL
    if year is None:
        # current month
        if period[0] == "" or period[1] == "":
            pass
        else:
            request_url_str += f"/{period[0]}/{period[1]}"
    elif year is not None:
        # specific year
        request_url_str += f"/{year}"
    else:
        # this is not good
        LOGGER.error(
            "Error while building request url this should not happen. We should have a year or not"
        )
        return dict()

    LOGGER.debug(f"Profile -- Request url: {request_url_str}")

    # validate the JSON response
    response = session.get(request_url_str)
    if response.status_code != 200:
        LOGGER.error(f"Error while fetching power data: {response.status_code}")
        return dict()
    response.json()

    data = response.json()
    # TODO validate the json data
    # try:
    #     validate(data, SCHEMA)
    # except ValidationError as e:
    #     LOGGER.error(e)
    #     return dict()

    return data
