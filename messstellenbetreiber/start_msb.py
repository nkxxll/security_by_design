import os
import sys
import subprocess

from messstellenbetreiber.simulationTools.simulationTooling import SimulationTooling
from messstellenbetreiber.intelligenterStromzähler.stromzahler import Stromzahler
from messstellenbetreiber.msbDatabase.databaseServer import DatabaseServer

msb_server = None


def start_msb(sqlite_file: str = "./msb.db"):
    global msb_server
    msb_server = DatabaseServer(sqlite_file)
    msb_server.start_server()


def stop_msb():
    pass


def restart_db():
    pass
