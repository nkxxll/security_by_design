# Readme fuer Kundenportal

## Migration

to migrade the new database pattern to the sqlite3 database just type `python3 manage.py migrate`
this initilizes the necessary databases in sqlite3

you can show the migration with the command `python3 manage.py makemigration <app>`
if you want to apply them then you can type `python3 manage.py sqlmigrate <app> <nr>`

## TODOs

- [ ] logout site?
- [ ] create index for Kundenportal
- [ ] profile view logout button login button clean up
- [ ] create user sign up site
- [ ] research session timeout in django

