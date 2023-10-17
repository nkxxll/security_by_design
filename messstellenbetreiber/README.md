messtellenbetreiber

Datenbank:
Tabellen:
- Kunde_Stromzähler Relationstabelle:
    - KundenId
    - StromzählerId
- Kunde Datentabelle:
    - KundenId
    - Straße
    - Hausnummer
    - Hausnummerzusatz
    - Postleitzahl
    - Stadtname
- Stromzähler_Strom Datentabelle:
    - StromzählerId
    - Stromverbrauch_gesamt # in Watt
    - Stromverbrauch_momentan (if possible) # in Watt
    - Uhrzeit # in sekunden seit 1970
- Stromzähler_Wartung Datentabelle:
    - StromzählerId
    - Einbau_datum # in sekunden seit 1970
    - letzte_manuelle_Ablese_datum # in sekunden seit 1970
    - letzte_Eichung_datum # in sekunden seit 1970
    - nächste_Wartung_datum # in sekunden seit 1970

SQL_Befehle:
Read stromverbrauch per Year:
"""
SELECT KundenId, sz.Stromverbrauch_gesamt, SUM(sz.Stromverbrauch_momentan) AS test FROM Stromzähler_Strom as sz INNER JOIN Kunde as k ON sz.StromzählerId=k.StromzählerId;
"""