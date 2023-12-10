import sqlite3
import random
import time
import datetime
import string
import math

import messstellenbetreiber.simulationTools.random_data as random_data


class RandomDataGenerator:
    _con: sqlite3.Connection

    def __init__(self, _con) -> None:
        self._con = _con

    def get_id_auth(self, stromzahler_id):
        return self._con.execute(
            "SELECT * FROM StromzahlerAuth WHERE StromzahlerID=?",
            (str(stromzahler_id),),
        ).fetchall()

    def generate_id(self):
        stromzahler_id = 1
        while self.get_id_auth(stromzahler_id) != []:
            stromzahler_id = random.randint(2, 10000000000)
        return stromzahler_id

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
        "stromzahler_id": 1,
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

    def __init__(
        self, sqlite_file: str = "./..\\msbDatabase\\msb.db", debug_vebrauch=False
    ) -> None:
        self.debug_vebrauch = debug_vebrauch
        self._con = sqlite3.connect(sqlite_file)
        self._random_data = RandomDataGenerator(self._con)

    def min_to_ms(self, minute: float) -> float:
        return minute * 60 * 1000

    def s_timestamp_to_str(self, timestamp: int) -> str:
        return datetime.date.fromtimestamp(timestamp / 1000).isoformat()

    def ns_timestamp_to_str(self, timestamp: int) -> str:
        return datetime.date.fromtimestamp(timestamp / 1000).isoformat()

    def delete_table(self, table_name):
        try:
            self._con.execute(f"DROP TABLE {table_name}")
        except sqlite3.OperationalError as e:
            print(f"{table_name} already did not exist")

    def reset_db(self):
        print("Resetting DB")
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
        print("Resetted DB")

    def add_stromzahler_auth(self, stromzahler_id, key):
        self._con.execute(
            "INSERT INTO StromzahlerAuth (StromzahlerID, Auth_Key) VALUES (?, ?)",
            (stromzahler_id, key),
        )

    def add_stromzahler_location(
        self, stromzahler_id, street, number, postleitzahl, stadtname
    ):
        self._con.execute(
            "INSERT INTO Position_Stromzahler (StromzahlerID,Straße, Hausnummer, Postleitzahl, Stadtname) VALUES (?, ?, ?, ?, ?)",
            (stromzahler_id, street, number, postleitzahl, stadtname),
        )

    def add_stromzahler_verbrauch(self, stromzahler_id, gesamt, time):
        self._con.execute(
            "INSERT INTO StromzahlerVerbrauch (StromzahlerID, StromverbrauchGesamt, Uhrzeit) VALUES (?, ?, ?)",
            (stromzahler_id, gesamt, time),
        )

    def add_stromzahler_wartung(
        self, stromzahler_id, einbau_datum, eichungs_datum, letzes_wartungs_datum
    ):
        self._con.execute(
            "INSERT INTO StromzahlerWartung (StromzahlerID,	Einbaudatum, letztesEichungsDatum, letzesWartungsDatum) VALUES (?, ?, ?, ?)",
            (stromzahler_id, einbau_datum, eichungs_datum, letzes_wartungs_datum),
        )

    def add_testcase_data(self):
        testid = self._test_object["stromzahler_id"]
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
        self._con.commit()

    def add_random_stromzahler(self, amount: int):
        for i in range(amount):
            # add authkey
            stromzahler_id = self._random_data.generate_id()
            authkey = self._random_data.generate_authkey()
            print(
                f"adding stromzahler stromzahler_id={stromzahler_id} ; auth={authkey}"
            )
            self.add_stromzahler_auth(stromzahler_id, authkey)
            # add random location
            random_position = self._random_data.generate_random_position()
            self.add_stromzahler_location(
                stromzahler_id,
                random_position[0],
                random_position[1],
                random_position[2],
                random_position[3],
            )
            # add einbau und wartungs dates
            random_einbau = int(
                round(self._random_data.generate_random_date([1, 1, 2019]) * 1000)
            )
            random_wartung = int(round(self._random_data.generate_random_date() * 1000))
            if random_einbau > random_wartung:
                random_wartung = random_einbau
            self.add_stromzahler_wartung(
                stromzahler_id, random_einbau, random_einbau, random_wartung
            )
            # add verbrauch
            now = int(round(time.time() * 1000))
            gesamt = 0
            step = math.ceil(self.min_to_ms(15))
            max_steps = 32600
            start = math.ceil(now) - (step * max_steps)
            end = math.ceil(now)
            if (end - random_einbau) / step < max_steps:
                start = random_einbau
            print(
                f"adding {(end-start)/step} entries from {self.ns_timestamp_to_str(start)} to {self.ns_timestamp_to_str(end)}"
            )
            for i in range(start, end, step):
                if i % self.min_to_ms(2000) <= step and self.debug_vebrauch:
                    print(
                        f"{int(((i-start) / (end-start))*100)}%, total entries: {math.ceil(now) - i / step}, step: {step}"
                    )
                self.add_stromzahler_verbrauch(stromzahler_id, gesamt, i)
                gesamt += random.randint(20, 800)
            self._con.commit()

    def get_stromzahler_data(self, stromzahler_id: int = 1, key: str = "testkey"):
        output = {}
        select_output: list = self._con.execute(
            "SELECT * FROM StromzahlerAuth WHERE StromzahlerID=?",
            (str(stromzahler_id),),
        ).fetchall()
        output["auth"] = select_output
        select_output: list = self._con.execute(
            "SELECT * FROM Position_Stromzahler WHERE StromzahlerID=?",
            (str(stromzahler_id),),
        ).fetchall()
        output["position"] = select_output
        select_output: list = self._con.execute(
            "SELECT * FROM StromzahlerWartung WHERE StromzahlerID=?",
            (str(stromzahler_id),),
        ).fetchall()
        output["wartung"] = select_output
        select_output: list = self._con.execute(
            "SELECT * FROM StromzahlerVerbrauch WHERE StromzahlerID=?",
            (str(stromzahler_id),),
        ).fetchall()
        output["verbrauch"] = select_output
        return output
