messtellenbetreiber

Datenbank:
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