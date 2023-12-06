import logging
import json
import sqlite3

DB_FILE = "./msb.db"


class DbConnector:
    _con: sqlite3.Connection

    def __init__(self) -> None:
        self._con = sqlite3.connect(DB_FILE)

    def does_auth_key_exist(self, auth_key: str) -> bool:
        output = self.get_auth_key_data(auth_key)
        return len(output) == 1

    def get_stromzahler_id_from_auth_key(self, auth_key: str) -> int:
        select_output: list = self.get_auth_key_data(auth_key)
        return int(select_output[0][0])

    def get_auth_key_data(self, auth_key: str) -> list[tuple[str]]:
        select_output: list = self._con.execute(
            "SELECT StromzahlerID FROM StromzahlerAuth WHERE Auth_Key = ?",
            (str(auth_key),),
        ).fetchall()
        return select_output

    def get_stromverbrauch_in_timeframe(
        self, stromzahler_id: str, start_timestamp: int, end_timestamp: int
    ) -> list[list[str]]:
        select_output: list = self._con.execute(
            """SELECT StromverbrauchGesamt, Uhrzeit
                FROM StromzahlerVerbrauch
                WHERE StromzahlerID = ?
                  AND Uhrzeit >= ? AND Uhrzeit <= ?""",
            (stromzahler_id, start_timestamp, end_timestamp),
        ).fetchall()
        return select_output

    def get_stromverbrauch(self, stromzahler_id: int) -> list[tuple[str]]:
        select_output: list = self._con.execute(
            """SELECT StromverbrauchGesamt, Uhrzeit FROM StromzahlerVerbrauch WHERE StromzahlerID = ?""",
            (stromzahler_id,),
        ).fetchall()
        return select_output

    def get_strom_wartung(self, stromzahler_id: int) -> list[tuple[str]]:
        select_output: list = self._con.execute(
            """SELECT Einbaudatum,letztesEichungsDatum,letzesWartungsDatum FROM StromzahlerWartung WHERE StromzahlerID=?""",
            (stromzahler_id,),
        ).fetchall()
        return select_output
