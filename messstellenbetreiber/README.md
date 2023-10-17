messtellenbetreiber

Datenbank:
Tabellen:
- Kunde Stromzähler Relationstabelle:
    - KundenId
    - StromzählerId
- Kunde Datentabelle:
    - KundenId
    - Straße
    - Hausnummer
    - Hausnummerzusatz
    - Postleitzahl
    - Stadtname
- Stromzähler Strom Datentabelle:
    - StromzählerId
    - Stromverbrauch_gesamt # in Watt
    - Stromverbrauch_momentan (if possible) # in Watt
    - Uhrzeit # in sekunden seit 1970
- Stromzähler Wartung Datentabelle:
    - StromzählerId
    - Einbau_datum # in sekunden seit 1970
    - letzte_manuelle_Ablese_datum # in sekunden seit 1970
    - letzte_Eichung_datum # in sekunden seit 1970
    - nächste_Wartung_datum # in sekunden seit 1970