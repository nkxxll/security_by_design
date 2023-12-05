# Readme fuer Kundenportal

## Documentation of the routes

- '/' index site a not authenticated user is able to sign up or login from here
if the use is logged in he is able to hit the logout button to logout
- '/logout' logs out a authenticated user and redirects to the index page
- '/login' has a form to log in to the page and authenticate yourself to the
server after authenticating the use is redirected to the account's profile site
- '/edit' lets the user edit their personal data
- '/signup' lets a user sign up to the portal by entering name, email and
password password should probably be validated for a specific complexity
    - if sign up is successful the user is redirected to his profile page
    else the user is not redirected and is able to try it again


## Migration

to migrade the new database pattern to the sqlite3 database just type `python3 manage.py migrate`
this initilizes the necessary databases in sqlite3

you can show the migration with the command `python3 manage.py makemigration <app>`
if you want to apply them then you can type `python3 manage.py sqlmigrate <app> <nr>`

## TODOs

- [x] logout site?
- [ ] create index for Kundenportal
- [ ] profile view logout button login button clean up
- [x] create user sign up site
- [ ] research session timeout in django

## generate a ssl cert with openssl

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
```

Run test server with SSL cert:

```bash
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
```
