import base64, io
from typing import Tuple
from logging import getLogger
from django.contrib.admin.options import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as lo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from jsonschema import validate, ValidationError
from power_data.models import PowerData
from datetime import datetime
import requests
from .utils.forms import CreateUserForm, CreateUserMeta, CreateEditData
import matplotlib
# use agg backend to prevent gui error
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator

# this is for the power data validation


LOGGER = getLogger(__name__)
SCHEMA = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://example.com/object1702208133.json",
    "title": "Root",
    "type": "array",
    "default": [],
    "items": {
        "$id": "#root/items",
        "title": "Items",
        "type": "object",
        "required": [],
        "properties": {
            "0": {
                "$id": "#root/items/0",
                "title": "0",
                "type": "integer",
                "examples": [15],
                "default": 0,
            }
        },
    },
}

MSB_PORT = 3000
MSB_HOST = "localhost"
MSB_API_ROUTE = "api/v1/stromverbrauch"
MSB_API_URL = f"http://{MSB_HOST}:{MSB_PORT}/{MSB_API_ROUTE}"


def index(request):
    LOGGER.info(f"index - Index page was requested by id: {request.user.id}")
    return render(request, "index.html", {})


def logout(request):
    lo(request)
    LOGGER.info(f"logout - User with the id: {request.user.id} logged out")
    return render(request, "logout.html", {})


def notfound(request):
    LOGGER.info(f"notfound - 404 page was requested by user with id: {request.user.id}")
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
            if edit_data_form.cleaned_data["password"] != "":
                request.user.set_password(edit_data_form.cleaned_data["password"])
            # update meta data
            power_data = PowerData.objects.get(user=request.user)
            power_data.street = edit_data_form.cleaned_data["street"]
            power_data.street_number = edit_data_form.cleaned_data["street_number"]
            power_data.postal_code = edit_data_form.cleaned_data["postal_code"]
            power_data.city = edit_data_form.cleaned_data["city"]
            if edit_data_form.cleaned_data["auth_key"] != "":
                power_data.auth_key = edit_data_form.cleaned_data["auth_key"]
            request.user.save()
            power_data.save()
            LOGGER.info(f"edit - User with the id: {request.user.id} edited his data")
            # update user data
            return HttpResponseRedirect("/profile", request)
        else:
            # return form error
            LOGGER.error(f"edit - User with the id: {request.user.id} failed to edit his data error: {edit_data_form.errors}")
            return render(
                request,
                template_name="edit.html",
                context={"edit_data_form": edit_data_form},
            )
    else:
        LOGGER.info(f"edit - User with the id: {request.user.id} requested the edit page")
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
            LOGGER.info(f"signup - User with the id: {request.user.id} signed up")
            return HttpResponseRedirect("/profile", request)
        else:
            # return form error
            LOGGER.error(f"signup - User with the id: {request.user.id} failed to sign up error:\n\tuser_data: {user_form.errors}\n\tmeta_data: {data_form.errors}")
            return render(
                request,
                template_name="signup.html",
                context={"user_form": user_form, "data_form": data_form},
            )
    else:
        user_form = CreateUserForm()
        data_form = CreateUserMeta()
        LOGGER.info(f"signup - User with the id: {request.user.id} requested the signup page")
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
    power_data["stromverbrauch_q423"] = _get_powerdata(
        request.user, ("2023-10-01", "2023-12-31")
    )
    context["power_data"] = power_data
    LOGGER.debug(context["power_data"])
    user_data = PowerData.objects.get(user=request.user)
    context["user_data"] = user_data

    values_alltime = []
    timestamps_alltime = []
    for i, val in enumerate(power_data["stromverbrauch"]):
        for j in val:
            values_alltime.append(val[j])
            timestamps_alltime.append(int(j))

    dates_alltime = [datetime.utcfromtimestamp(ts / 1000) for ts in timestamps_alltime]

    fig_alltime, ax_alltime = plt.subplots(figsize=(10,4))
    ax_alltime.plot(dates_alltime, values_alltime, '--bo')

    fig_alltime.autofmt_xdate()
    ax_alltime.set_title('By date')
    ax_alltime.set_ylabel("Data")
    ax_alltime.set_xlabel("Timestamp")
    ax_alltime.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
    ax_alltime.yaxis.set_minor_locator(LinearLocator(25))
    plt.savefig('books_read.png')

    flike_alltime = io.BytesIO()
    fig_alltime.savefig(flike_alltime)
    b64_alltime = base64.b64encode(flike_alltime.getvalue()).decode()
    context['chart_alltime'] = b64_alltime

    values_q423 = []
    timestamps_q423 = []
    for i, val in enumerate(power_data["stromverbrauch_q423"]):
        for j in val:
            values_q423.append(val[j])
            timestamps_q423.append(int(j))

    dates_q423 = [datetime.utcfromtimestamp(ts / 1000) for ts in timestamps_q423]

    fig_q423, ax_q423 = plt.subplots(figsize=(10,4))
    ax_q423.plot(dates_q423, values_q423, '--bo')

    fig_q423.autofmt_xdate()
    ax_q423.set_title('By date')
    ax_q423.set_ylabel("Data")
    ax_q423.set_xlabel("Timestamp")
    ax_q423.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)
    ax_q423.yaxis.set_minor_locator(LinearLocator(25))

    flike_q423 = io.BytesIO()
    fig_q423.savefig(flike_q423)
    b64_q423 = base64.b64encode(flike_q423.getvalue()).decode()
    context['chart_q423'] = b64_q423

    LOGGER.info(f'{context["power_data"]}')

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

    LOGGER.info(f"_get_powerdata -- Request url: {request_url_str}")

    # validate the JSON response
    response = session.get(request_url_str)
    if response.status_code != 200:
        LOGGER.error(f"Error while fetching power data: {response.status_code}")
        return dict()
    response.json()

    data = response.json()
    # TODO validate the json data
    try:
        validate(data, SCHEMA)
        LOGGER.info("_get_powerdata - Power data validated successfully")
    except ValidationError as e:
        LOGGER.error(f"_get_powerdata - Error while validating power data: {e}")
        return dict()

    return data
