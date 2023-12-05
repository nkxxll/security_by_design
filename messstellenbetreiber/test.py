import unittest
from requests.cookies import RequestsCookieJar
from requests import get


class Unittest(unittest.TestCase):
    def all_existing_data(self):
        cookies: RequestsCookieJar = RequestsCookieJar()
        cookies.set("auth_key", "testkey")
        db_output = 
        data = get( 
            "http://localhost:3000/api/v1/stromverbrauch/read_Stromverbrauch_all",
            cookies=cookies,
        )
        self.assertEqual(data, db_output)

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
