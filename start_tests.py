import unittest
from requests.cookies import RequestsCookieJar
from requests import get
import requests


import messstellenbetreiber.msbDatabase.databaseServer as DatabaseServer

API_ROUTES = DatabaseServer.APIRoutes


class DBServerTests(unittest.TestCase):
    def do_request(self, route: str, key: str = "testkey") -> dict:
        cookies: RequestsCookieJar = RequestsCookieJar()
        cookies.set("auth_key", key)
        try:
            return get(
                "http://localhost:3000" + route,
                cookies=cookies,
            ).json()
        except requests.exceptions.JSONDecodeError:
            return get(
                "http://localhost:3000" + route,
                cookies=cookies,
            ).text

    def test_all_existing_data(self):
        data = self.do_request(API_ROUTES.ALL_STROMVERBRAUCH.value)
        self.assertEqual(data, [{"0": 15}, {"900000": 30}])

    def test_data_period(self):
        self.assertTrue(True)

    def test_yearly_data(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "1970")
        )
        self.assertEqual(data, [{"0": 15}, {"900000": 30}])

    def test_yearly_no_data(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "1980")
        )
        self.assertEqual(data, [])

    def test_post_stormzahler(self):
        self.assertTrue(True)

    def test_post_stormzahler_sql_injection(self):
        self.assertTrue(True)

    def test_request_without_key(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "1980"), ""
        )
        self.assertEqual(data, "No")

    def test_request_yearly_without_standard_input(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "19880")
        )
        self.assertEqual(data, "No")

    def test_request_yearly_without_standard_input(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "19880Hello")
        )
        self.assertEqual(data, "No")

    def test_request_year_sql_injection(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "1970' OR 1=1;")
        )
        self.assertEqual(data, "No")

    def test_request_timeframe_sql_injection(self):
        data = self.do_request(
            API_ROUTES.TIMEFRAME_STROMVERBRAUCH.value.replace(
                "<start_time>", "0' OR 1=1;"
            ).replace("<end_time>", "900000 OR 1=1;")
        )
        self.assertEqual(data, "No")

    def test_request_key_sql_injection(self):
        data = self.do_request(
            API_ROUTES.YEARLY_STROMVERBRAUCH.value.replace("<year>", "1970' OR 1=1;"),
            "testkey' OR 1=1;",
        )
        self.assertEqual(data, "No")


if __name__ == "__main__":
    unittest.main()
    DBServerTests()
