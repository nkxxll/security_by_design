import sys
import logging
import json
import time
from enum import Enum
from flask import Flask, request

from dbConnection import DbConnector

# add log-file
logging.basicConfig(
    filename="http_api.log",
    encoding="utf-8",
    level=logging.DEBUG,
)
# add console-log
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stderr))

app = Flask(__name__)

API_ROUTE = "/api/v1/"
HOST = "localhost"
PORT = 3000


class HTTPCodes(Enum):
    DEFAULT = 200
    NOT_ALLOWED = 404


NOT_ALLOWED_MESSAGE = "No"


def convert_verbrauch_data_to_response(data: list[tuple]):
    result = []
    # row[1] is timestamp
    # row[0] is verbrauchs value
    for row in data:
        result.append({row[1]: row[0]})
    return result


def date_to_timestamp(year: str, month: str = 1, day: str = 1) -> int:
    if int(year) < 1971:
        return 0
    return int(
        round(time.mktime(time.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")) * 1000)
    )


@app.route("/", methods=["GET"])
def index():
    return "Hello th the server"


@app.route(API_ROUTE, methods=["GET"])
def api_index():
    return "Hello to The API"


@app.errorhandler(404)
def not_found(error):
    return "Not allowed", 404


@app.route(API_ROUTE + "stromverbrauch", methods=["GET"])
def show_verbrauch_all():
    response_message = "not implemented"
    response_code = HTTPCodes.DEFAULT
    db: DbConnector = DbConnector()
    if not db.does_auth_key_exist(request.cookies.get("auth_key")):
        response_message = NOT_ALLOWED_MESSAGE
        response_code = HTTPCodes.NOT_ALLOWED
    else:
        auth_key = request.cookies.get("auth_key")
        stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
        data = db.get_stromverbrauch(stromzahler_id)
        response_message = convert_verbrauch_data_to_response(data)
    return response_message, response_code.value


@app.route(API_ROUTE + "stromverbrauch/<year>", methods=["GET"])
def show_verbrauch_year(year):
    response_message = "not implemented"
    response_code = HTTPCodes.DEFAULT
    db: DbConnector = DbConnector()
    if not db.does_auth_key_exist(request.cookies.get("auth_key")):
        response_message = NOT_ALLOWED_MESSAGE
        response_code = HTTPCodes.NOT_ALLOWED
    else:
        auth_key = request.cookies.get("auth_key")
        stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
        start_time = date_to_timestamp(year)
        end_time = time.time()
        data = db.get_stromverbrauch_in_timeframe(stromzahler_id, start_time, end_time)
        response_message = convert_verbrauch_data_to_response(data)
    return response_message, response_code.value


@app.route(API_ROUTE + "stromverbrauch/<start_time>/<end_time>", methods=["GET"])
def show_verbrauch_timeframe(start_time, end_time):
    response_message = "not implemented"
    response_code = HTTPCodes.DEFAULT
    db: DbConnector = DbConnector()
    if not db.does_auth_key_exist(request.cookies.get("auth_key")):
        response_message = NOT_ALLOWED_MESSAGE
        response_code = HTTPCodes.NOT_ALLOWED
    else:
        auth_key = request.cookies.get("auth_key")
        stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
        data = db.get_stromverbrauch_in_timeframe(stromzahler_id, start_time, end_time)
        response_message = convert_verbrauch_data_to_response(data)
    return response_message, response_code.value


app.run(HOST, PORT)
