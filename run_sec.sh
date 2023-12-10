#!/usr/bin/env bash

# start the simulation of the msb server
python3 ./start_simulation.py

# start the kundenportalserver in a secure way with the wsgi server
gunicorn -b

