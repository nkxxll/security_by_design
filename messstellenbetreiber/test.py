import unittest
from requests.cookies import RequestsCookieJar
from requests import get

import messstellenbetreiber.msbDatabase.databaseServer as DatabaseServer

API_ROUTES = DatabaseServer.APIRoutes


class DBServerTests(unittest.TestCase):
    def do_request(self, route: str) -> dict:
        cookies: RequestsCookieJar = RequestsCookieJar()
        cookies.set("auth_key", "testkey")
        return get(
            "http://localhost:3000" + route,
            cookies=cookies,
        ).json()

    def all_existing_data(self):
        data = self.do_request(API_ROUTES.ALL_STROMVERBRAUCH.value)
        print(data)
        self.assertEqual(data, "db_output")

    def data_period(self):
        self.assertTrue(True)

    def yearly_data(self):
        self.assertTrue(True)

    def monthly_data(self):
        self.assertTrue(True)

    def request_safe_new_data(self):
        self.assertTrue(True)

    def request_safe_new_data_failed(self):
        self.assertTrue(True)

    def request_without_key(self):
        self.assertTrue(True)

    def request_without_standard_input(self):
        self.assertTrue(True)

    def request_without_standard_input(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
