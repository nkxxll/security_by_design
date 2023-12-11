# Security By Design Projektentwurf

Dies ist der Projektentwurf für den Kurs Security by Design.

## Building the Project

### Installation of Requirements

```bash
# optional
python3 -m venv env
./env/bin/activate
# requirements
python3 -m pip install -r requirements.txt
```

### Start the Application

Before starting the application you have to migrate the Django database schema.
You can do that with the following command.

```bash
cd ./kundenportal/kp_app/
python3 manage.py migrate
```

Then run the server with this command (in dev mode).

```bash
bash -c run.sh
# or
./run.sh
```

### Start the Application in a secure manner

1. Generate a SSL certificate with OpenSSL

```bash
# generate ssl key and cert
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
# remove the encryption from the key because gunicorn does not support that (yes that is unsecure
# you should normally not do that; just for the presentation of the project here)
openssl rsa -in key.pem -out easy_key.pem
```
Now move the `easy_key.pem` and `cert.pem` file into the `kp_app` dir.

Please keep in mind that the key is not signed and you browser will warn you about that.
You could sign the key with the help of [Let's Encrypt](https://letsencrypt.org/).

2. Edit the settings for the Django server to be secure. To do that navigate
   with the editor of choice to the `settings.py` file in the location
   `./kundenportal/kp_app/kundenportal/settings.py` and change the following constants.

```python
DEBUG = False # this should be false in production
# here you would find the address of the Messstellenbetreiber Server in this
# case the server is running on the same system hence "localhost"
ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]"]
# ...
# === Security Settings ===
# NOTE: this is a low value for testing can be higher in production please keep
# that value at 0 because the browser cache is memorizing that value you cannot
# switch between only ssl and an insecure connection without deleting the browser
# cache
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # this should be set to true in production
SECURE_HSTS_PRELOAD = True # this should be set to true in production
SECURE_SSL_REDIRECT =  True # this should be set to true in production
SESSION_COOKIE_SECURE = True # this should be set to true
CSRF_COOKIE_SECURE = True # this should be set to true
```

[What are those settins](https://docs.djangoproject.com/en/5.0/topics/security/)

3. Take out the admin site we only need it for developement in production. This site is just an attack vector that is not necessary. For that go to the `urls.py` and comment out this protion.

```python
urlpatterns = [
    # path("admin/", admin.site.urls), # this needs to be commented out in production no need for an admin site
    path("", views.index, name="index"),
# ...
]
```

4. Start the server with [gunicorn](https://gunicorn.org/) and an SSL certificate as well as an SSL key.

```bash
bash -c run_sec.sh
# or
./run_sec.sh
```

## Info for Test Users

Test users have to be create manually. Go to `/singup` and enter some nice mock
infos. If you want to have some mock data as well look at the "test auth keys"
that are displayed when starting the Messstellenbetreiber Server and enter one
of them in the sing up mask. Now just log in your user.
