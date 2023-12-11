#!/usr/bin/env bash

# start the simulation of the msb server
echo "=== Starting Messstellenbetreiber web server ==="
echo "===! There are some test auth_keys you can use with some test users that you are able to create !==="
python3 ./start_simulation.py

# start the kundenportalserver in a secure way with the wsgi server
cd ./kundenportal/kp_app
echo "=== Changed directory to $(pwd) ==="

echo "=== Starting kundenportal with gunicorn. Cert: $(pwd)/cert.pem. Key: $(pwd)/key.pem ==="
echo "===! The key file is not encrypted this is a possible security issue gunicorn unfortunately does not support encrypted key files !==="
gunicorn --certfile=cert.pem --keyfile=easy_key.pem kundenportal.wsgi

cd ../../
echo "=== Changed directory back to $(pwd) ==="
