#!/usr/bin/env bash

# start the simulation of the msb server
echo "=== Starting Messstellenbetreiber web server ==="
echo "===! There are some test auth_keys you can use with some test users that you are able to create !==="
python3 ./start_simulation.py

# start the kundenportalserver in a secure way with the wsgi server
cd ./kundenportal/kp_app
echo "=== Changed directory to $(pwd) ==="

echo "=== Starting kundenportal with the dev server ==="
python3 manage.py runserver

cd ../../
echo "=== Changed directory back to $(pwd) ==="
