# Kundenportal
# Kundenportal-Messstellenbetreiber Schnittstelle
- signed Cookies
  - https://expressjs.com/en/5x/api.html#req.signedCookies
  - glaube bei django ist es das: https://docs.djangoproject.com/en/4.2/topics/signing/
- simulation befüllen kundenportalseitig : in klärung
  - python script oder sowas which takes as args: [zahlerKey, Street, Housenumber, PLZ, City]
  - python script adds this data to his db and randomly generates names and all other necessary data
# Messstellenbetreiber
## Simulationspopulation
- sql commands to
  - [X] fill stromzähler location tabelle : started
  - [X] fill stromzähler id key relation tabelle (auth tabelle)
  - fill stromzähler wartung tabelle
  - fill stormzähler verbrauch tabelle : done in intelligenter Stromzähler
- [X] zusammenfügen dieser SQL Commands um ein neuen Stromzähler mit einer bestimmten Menge an Daten zu generieren : in klärung
- [X] generierung von vielen Stromzählern (5000 oder so)
## Database API 
- automatic api tests via a python script or smth
- check config via schema validation
## intelligenter Stromzähler
- check config via schema validation
## Wartungsportal
- erfragen ob es einen mehrwert hat es zu erstellen
- hoffen dass wirs lassen können
- erfragen ob bei der registrierung beim kundenportal automatisch ein neuer stormzähler für den kunden erstellt werden soll
- wenn das der Fall ist, ist es auch sinnvoller, einfach ne menge registrierungen zu simulieren und dann dem msb zu sagen "mach mal da random beispieldaten für"git 