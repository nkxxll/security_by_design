import sqlite3
import random
import time
import datetime
import string
import math

import random_data


class RandomDataGenerator:
    _con: sqlite3.Connection

    def __init__(self, _con) -> None:
        self._con = _con

    def get_id_auth(self, id):
        return self._con.execute(
            "SELECT * FROM StromzahlerAuth WHERE StromzahlerID=?", (str(id),)
        ).fetchall()

    def generate_id(self):
        id = 1
        while self.get_id_auth(id) != []:
            id = random.randint(2, 10000000000)
        return id

    def get_auth_id(self, authkey):
        return self._con.execute(
            "SELECT * FROM StromzahlerAuth WHERE Auth_Key=?", (str(authkey),)
        ).fetchall()

    def generate_authkey(self):
        letters = string.ascii_letters
        letters += "0123456789"
        letters += ",.-_+*#!$%&"
        authkey = "testkey"
        while self.get_auth_id(authkey) != []:
            authkey = "".join(random.choice(letters) for i in range(18))
        return authkey

    def generate_random_position(self):
        streetname = random.choice(random_data.STREET_NAMES)
        housenumber = random.randint(1, 300)
        postleitzahl = random.randint(10000, 99999)
        cityname = random.choice(random_data.CITY_NAMES)

        return [streetname, housenumber, postleitzahl, cityname]

    def generate_random_date(
        self,
        startdate: list = [1, 1, 2023],
        enddate: list = [29, 11, 2023],
        get_timestamp=True,
    ):
        day = random.randint(startdate[0], enddate[0])
        month = random.randint(startdate[1], enddate[1])
        year = random.randint(startdate[2], enddate[2])
        if get_timestamp:
            return time.mktime(time.strptime(f"{year}-{month}-{day}", "%Y-%m-%d"))
        else:
            return [day, month, year]


class SimulationTooling:
    _con: sqlite3.Connection
    _random_data: RandomDataGenerator
    _test_object = {
        "id": 1,
        "key": "testkey",
        "location": {
            "street": "teststraße",
            "number": 1,
            "postleitzahl": 11111,
            "stadtname": "teststadt",
        },
        "verbrauch": {0: 15, 900000: 30},
        "all_dates": 10000,
    }

    def __init__(self) -> None:
        self._con = sqlite3.connect("./..\\msbDatabase\\msb.db")
        self._random_data = RandomDataGenerator(self._con)

    def min_to_ms(self, minute: float) -> float:
        return minute * 60 * 1000

    def delete_table(self, table_name):
        try:
            self._con.execute(f"DROP TABLE {table_name}")
        except sqlite3.OperationalError as e:
            print(f"{table_name} already did not exist")

    def reset_db(self):
        self.delete_table("Position_Stromzahler")
        self.delete_table("StromzahlerAuth")
        self.delete_table("StromzahlerWartung")
        self.delete_table("StromzahlerVerbrauch")
        self._con.execute(
            """CREATE TABLE Position_Stromzahler (
                StromzahlerID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                Straße TEXT, 
                Hausnummer INTEGER,
                Hausnummerzusatz TEXT,
                Postleitzahl INTEGER,
                Stadtname TEXT);"""
        )
        self._con.execute(
            """CREATE TABLE StromzahlerAuth  (
                StromzahlerID INTEGER,
                Auth_Key TEXT UNIQUE PRIMARY KEY,
                FOREIGN KEY (StromzahlerID) REFERENCES Position_Stromzahler(StromzahlerID));"""
        )
        self._con.execute(
            """CREATE TABLE StromzahlerWartung (
                StromzahlerID INTEGER,
                Einbaudatum INTEGER,
                letztesEichungsDatum INTEGER,
                letzesWartungsDatum INTEGER,
                FOREIGN KEY (StromzahlerID) REFERENCES Position_Stromzahler(StromzahlerID));"""
        )
        self._con.execute(
            """CREATE TABLE StromzahlerVerbrauch (
                StromzahlerID INTEGER,
                StromverbrauchGesamt INTEGER,
                StromverbrauchJetzt INTEGER,
                Uhrzeit INTEGER,
                FOREIGN KEY (StromzahlerID) REFERENCES Position_Stromzahler(StromzahlerID));"""
        )
        self._con.commit()

    def add_stromzahler_auth(self, id, key):
        self._con.execute(
            "INSERT INTO StromzahlerAuth (StromzahlerID, Auth_Key) VALUES (?, ?)",
            (id, key),
        )
        self._con.commit()

    def add_stromzahler_location(self, id, street, number, postleitzahl, stadtname):
        self._con.execute(
            "INSERT INTO Position_Stromzahler (StromzahlerID,Straße, Hausnummer, Postleitzahl, Stadtname) VALUES (?, ?, ?, ?, ?)",
            (id, street, number, postleitzahl, stadtname),
        )
        self._con.commit()

    def add_stromzahler_verbrauch(self, id, gesamt, time):
        self._con.execute(
            "INSERT INTO StromzahlerVerbrauch (StromzahlerID, StromverbrauchGesamt, Uhrzeit) VALUES (?, ?, ?)",
            (id, gesamt, time),
        )
        self._con.commit()

    def add_stromzahler_wartung(
        self, id, einbau_datum, eichungs_datum, letzes_wartungs_datum
    ):
        self._con.execute(
            "INSERT INTO StromzahlerWartung (StromzahlerID,	Einbaudatum, letztesEichungsDatum, letzesWartungsDatum) VALUES (?, ?, ?, ?)",
            (id, einbau_datum, eichungs_datum, letzes_wartungs_datum),
        )
        self._con.commit()

    def add_testcase_data(self):
        testid = self._test_object["id"]
        self.add_stromzahler_auth(testid, self._test_object["key"])
        loc_data = self._test_object["location"]
        self.add_stromzahler_location(
            testid,
            loc_data["street"],
            loc_data["number"],
            loc_data["postleitzahl"],
            loc_data["stadtname"],
        )
        for key in self._test_object["verbrauch"].keys():
            self.add_stromzahler_verbrauch(
                testid, self._test_object["verbrauch"][key], key
            )
        self.add_stromzahler_wartung(
            testid,
            self._test_object["all_dates"],
            self._test_object["all_dates"],
            self._test_object["all_dates"],
        )

    def add_random_stromzahler(self, amount: int):
        for i in range(amount):
            id = self._random_data.generate_id()
            authkey = self._random_data.generate_authkey()
            print(f"adding stromzahler id={id} ; auth={authkey}")
            self.add_stromzahler_auth(id, authkey)
            random_position = self._random_data.generate_random_position()
            self.add_stromzahler_location(
                id,
                random_position[0],
                random_position[1],
                random_position[2],
                random_position[3],
            )
            random_einbau = self._random_data.generate_random_date([1, 1, 2019])
            random_wartung = self._random_data.generate_random_date()
            self.add_stromzahler_wartung(
                id, random_einbau, random_einbau, random_wartung
            )
            now = int(round(time.time() * 1000))
            gesamt = 0
            step = math.ceil(self.min_to_ms(15))
            start = math.ceil(now) - (step * 1000)
            end = math.ceil(now)
            print(
                f"adding {(end-start)/step} entries from {datetime.date.fromtimestamp(start/1000).isoformat()} to {datetime.date.fromtimestamp(end/1000).isoformat()}"
            )
            # TODO: make this proper from eibnau date to now in dynamic steps to not have 10000000000 entries
            for i in range(start, end, step):
                if i % self.min_to_ms(2000) <= step and debug_vebrauch:
                    print(
                        f"{int(((i-start) / (end-start))*100)}%, total entries: {math.ceil(now) - i / step}, step: {step}"
                    )
                self.add_stromzahler_verbrauch(id, gesamt, i)
                gesamt += random.randint(20, 800)

    def get_stromzahler_data(self, id: int = 1, key: str = "testkey"):
        output = {}
        select_output: list = self._con.execute(
            "SELECT * FROM StromzahlerAuth WHERE StromzahlerID=?", (str(id),)
        ).fetchall()
        output["auth"] = select_output
        select_output: list = self._con.execute(
            "SELECT * FROM Position_Stromzahler WHERE StromzahlerID=?", (str(id),)
        ).fetchall()
        output["position"] = select_output
        select_output: list = self._con.execute(
            "SELECT * FROM StromzahlerWartung WHERE StromzahlerID=?", (str(id),)
        ).fetchall()
        output["wartung"] = select_output
        select_output: list = self._con.execute(
            "SELECT * FROM StromzahlerVerbrauch WHERE StromzahlerID=?", (str(id),)
        ).fetchall()
        output["verbrauch"] = select_output
        return output


debug_vebrauch = False


def __main__():
    tools: SimulationTooling = SimulationTooling()
    tools.reset_db()
    tools.add_testcase_data()
    tools.add_random_stromzahler(8)


if __name__ == "__main__":
    __main__()
