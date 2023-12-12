#!/usr/bin/env bash

# start the simulation of the msb server
echo "=== Starting Messstellenbetreiber web server ==="
echo "===! There are some test auth_keys you can use with some test users that you are able to create !==="
python3 ./start_simulation.py & simulation_pid=$!

# start the kundenportalserver in a secure way with the wsgi server
cd ./kundenportal/kp_app || exit
echo "=== Changed directory to $(pwd) ==="

echo "=== Starting kundenportal with the dev server ==="
python3 manage.py runserver & kp_pid=$!

cd ../../
echo "=== Changed directory back to $(pwd) ==="

# kill the simulation and the kundenportalserver when the script is stopped
sleep 5
read -r -p "=== Press enter to stop the simulation and the kundenportalserver ==="
trap 'kill $simulation_pid $kp_pid' EXIT
