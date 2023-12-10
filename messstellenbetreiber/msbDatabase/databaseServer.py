import sys
import logging
import json
import time
from enum import Enum
from flask import Flask, request

from messstellenbetreiber.msbDatabase.dbConnection import DbConnector


class APIRoutes(Enum):
    API_ROUTE = "/api/v1/"
    ALL_STROMVERBRAUCH = API_ROUTE + "stromverbrauch"
    YEARLY_STROMVERBRAUCH = API_ROUTE + "stromverbrauch/<year>"
    TIMEFRAME_STROMVERBRAUCH = API_ROUTE + "stromverbrauch/<start_time>/<end_time>"
    UPDATE_LOCATION = API_ROUTE + "location"


class HTTPCodes(Enum):
    DEFAULT = 200
    NOT_ALLOWED = 404


class DatabaseServer:
    NOT_ALLOWED_MESSAGE = "No"
    HOST = "localhost"
    PORT = 3000
    app: Flask

    def __init__(self, sqlite_file: str = "./..\\msbDatabase\\msb.db") -> None:
        self.sqlite_file = sqlite_file
        # add log-file
        logging.basicConfig(
            filename="http_api.log",
            encoding="utf-8",
            level=logging.DEBUG,
        )
        # add console-log
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stderr))

        self.app = Flask(__name__)

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
                round(
                    time.mktime(time.strptime(f"{year}-{month}-{day}", "%Y-%m-%d"))
                    * 1000
                )
            )

        @self.app.route("/", methods=["GET"])
        def index():
            return "Hello th the server"

        @self.app.route(APIRoutes.API_ROUTE.value, methods=["GET"])
        def api_index():
            return "Hello to The API"

        @self.app.errorhandler(404)
        def not_found(error):
            return "Not allowed", 404

        @self.app.route(APIRoutes.ALL_STROMVERBRAUCH.value, methods=["GET"])
        def show_verbrauch_all():
            response_message = "not implemented"
            response_code = HTTPCodes.DEFAULT
            db: DbConnector = DbConnector(self.sqlite_file)
            if not db.does_auth_key_exist(request.cookies.get("auth_key")):
                response_message = self.NOT_ALLOWED_MESSAGE
                response_code = HTTPCodes.NOT_ALLOWED
            else:
                auth_key = request.cookies.get("auth_key")
                stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
                data = db.get_stromverbrauch(stromzahler_id)
                response_message = convert_verbrauch_data_to_response(data)
            return response_message, response_code.value

        @self.app.route(APIRoutes.YEARLY_STROMVERBRAUCH.value, methods=["GET"])
        def show_verbrauch_year(year):
            response_message = "not implemented"
            response_code = HTTPCodes.DEFAULT
            db: DbConnector = DbConnector(self.sqlite_file)
            if not db.does_auth_key_exist(request.cookies.get("auth_key")):
                response_message = self.NOT_ALLOWED_MESSAGE
                response_code = HTTPCodes.NOT_ALLOWED
            else:
                auth_key = request.cookies.get("auth_key")
                stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
                try:
                    start_time = date_to_timestamp(year)
                except ValueError:
                    # this handles a non integer input
                    response_message = self.NOT_ALLOWED_MESSAGE
                    response_code = HTTPCodes.NOT_ALLOWED
                    return response_message, response_code.value
                end_time = time.time()
                data = db.get_stromverbrauch_in_timeframe(
                    stromzahler_id, start_time, end_time
                )
                response_message = convert_verbrauch_data_to_response(data)
            return response_message, response_code.value

        @self.app.route(APIRoutes.TIMEFRAME_STROMVERBRAUCH.value, methods=["GET"])
        def show_verbrauch_timeframe(start_time, end_time):
            response_message = "not implemented"
            response_code = HTTPCodes.DEFAULT
            db: DbConnector = DbConnector(self.sqlite_file)
            if not db.does_auth_key_exist(request.cookies.get("auth_key")):
                response_message = self.NOT_ALLOWED_MESSAGE
                response_code = HTTPCodes.NOT_ALLOWED
            else:
                auth_key = request.cookies.get("auth_key")
                stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
                try:
                    start_time_dict = start_time.split("-")
                    start_time = date_to_timestamp(
                        start_time_dict[0], start_time_dict[1], start_time_dict[2]
                    )
                    end_time_dict = end_time.split("-")
                    end_time = date_to_timestamp(
                        end_time_dict[0], end_time_dict[1], end_time_dict[2]
                    )
                except ValueError:
                    # this handles a non integer input
                    response_message = self.NOT_ALLOWED_MESSAGE
                    response_code = HTTPCodes.NOT_ALLOWED
                    return response_message, response_code.value
                data = db.get_stromverbrauch_in_timeframe(
                    stromzahler_id, start_time, end_time
                )
                response_message = convert_verbrauch_data_to_response(data)
            return response_message, response_code.value

        @self.app.route(APIRoutes.UPDATE_LOCATION.value, methods=["POST"])
        def update_location():
            response_message = "not implemented"
            response_code = HTTPCodes.DEFAULT
            db: DbConnector = DbConnector(self.sqlite_file)
            if not db.does_auth_key_exist(request.cookies.get("auth_key")):
                response_message = self.NOT_ALLOWED_MESSAGE
                response_code = HTTPCodes.NOT_ALLOWED
            else:
                auth_key = request.cookies.get("auth_key")
                stromzahler_id = db.get_stromzahler_id_from_auth_key(auth_key)
                try:
                    start_time = int(start_time)
                    end_time = int(end_time)
                except ValueError:
                    # this handles a non integer input
                    response_message = self.NOT_ALLOWED_MESSAGE
                    response_code = HTTPCodes.NOT_ALLOWED
                    return response_message, response_code.value
                data = db.get_stromverbrauch_in_timeframe(
                    stromzahler_id, start_time, end_time
                )
                response_message = convert_verbrauch_data_to_response(data)
            response_message = "not implemented"
            return response_message, response_code.value

    def start_server(self):
        self.app.run(self.HOST, self.PORT)
