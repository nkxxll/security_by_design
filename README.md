# Security By Design Projektentwurf

Dies ist der Projektentwurf für den Kurs Security by Design.

## Building the Project

### Installation der Requirements

```bash
# optional
python3 -m venv env
./env/bin/activate
# requirements
python3 -m pip install -r requirements.txt
```

### Starten der Application

```bash
bash -c run.sh
```

### Starten der Application in einer sicheren weise

1. generate a SSL certificate with OpenSSL

```bash
# generate ssl key and cert
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
# remove the encryption from the key because gunicorn does not support that (yes that is unsecure
# you should normally not do that; just for the presentation of the project here)
openssl rsa -in key.pem -out easy_key.pem
```
2. move the `easy_key.pem` and `cert.pem` file into the `kp_app` dir

```bash
bash -c run_sec.sh
```

## Info zu den Testbenutzern

## To be done
