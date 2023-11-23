# messtellenbetreiber
### Anforderungen
- Baut Stromzähler ein
- Betreibt Stromzähler
- Wartet Stromzähler
- steht in der Stromrechnung
- Annahme: jeder Kunde hat bereits einen intelligenten Stromzähler mit Gateway weil wir zu viel geld haben
- 

# Betreiber
## Datenbank:
Tabellen:
- Kunde_Stromzähler Relationstabelle:
    - KundenID
    - StromzählerID
- Kunde Datentabelle:
    - KundenID
    - Straße
    - Hausnummer
    - Hausnummerzusatz
    - Postleitzahl
    - Stadtname
- Stromzähler_Verbrauch Datentabelle:
    - StromzählerID
    - Stromverbrauch_gesamt # in Watt
    - Stromverbrauch_momentan (if possible) # in Watt
    - Uhrzeit # in sekunden seit 1970
- Stromzähler_Wartung Datentabelle:
    - StromzählerID
    - Einbau_datum # in sekunden seit 1970
    - letzte_manuelle_Ablese_datum # in sekunden seit 1970
    - letzte_Eichung_datum # in sekunden seit 1970
    - nächste_Wartung_datum # in sekunden seit 1970
SQL_Befehle:
Read stromverbrauch per Year:
"""
SELECT KundenID, sz.Stromverbrauch_gesamt, SUM(sz.Stromverbrauch_momentan) AS test FROM Stromzähler_Verbrauch as sz INNER JOIN Kunde_Stromzähler as k ON sz.StromzählerID=k.StromzählerID;
"""
## Endpoints/API
### Anforderungen
- gibt aus wie viel Strom in einem Zeitraum ein Stromzähler verbraucht hat
- gibt Vertragsdaten zu einem bestimmten Vertrags eines Kunden aus
- gibt persönliche Daten eines Kunden aus Möglichkeit, persönliche Daten abzuändern
- 


# intelligenter Stromzähler Sim:
### Anforderungen:
- jeder Stromzähler benötigt ein Digitales Display
- Muss Kommunkationsfähig über das Internet sein
- Integration von Firewall Mechanismen
- Kommunikationsverbindungen ausschließlich von innen nach außen
- Authentifizierung, Verschlüsselung und Integritätssicherung jeglicher Kommunikation
- nutzen Simkarten aka. LTE für Internetverbindung
- Zählerstand wird alle 15 Minuten an den Betreiber gesendet


# text über die verwendeten Tools (JS, Express, python, Django)
siehe google docs