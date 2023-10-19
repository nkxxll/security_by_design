const sqlite3 = require('sqlite3');

class dbConnector {
    db_connection;
    constructor(db_type, db_location) {
        if (db_type == "sqlite" || db_type == "sqlite3") {
            this.db_connection = new sqlite3.Database(db_location, (err) => {
                if (err) {
                    console.error(err.message);
                }
                console.log('Connected to the sqlite database.');
            });
        }
        else if (db_type == "mysql" || db_type == "Mysql") {
            this.db_connection = "NOT IMPLEMENTED";
        }
    }

    /* Stromverbrauch von einer bestimmten Zeitspanne */
    read_Stromverbrauch_Year(kunde, zeitspanne_anfang, zeitspanne_ende) {
        this.db_connection.serialize(() => {
            this.db_connection.each(`SELECT KundenID,
                        sz.Stromverbrauch_gesamt, 
                        SUM(sz.Stromverbrauch_momentan) AS test 
                    FROM Stromzähler_Verbrauch as sz 
                    INNER JOIN Kunde_Stromzähler as k 
                    ON sz.StromzählerID=k.StromzählerID
                    WHERE KundenID = ?
                        AND Uhrzeit < ? AND Uhrzeit > ?`,
                [kunde, zeitspanne_anfang, zeitspanne_ende],
                (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    console.log(row.id + "\t" + row.name);
                });
        });
    }

    /* Stromverbrauch gesamt seid Vertragsbeginn */
    read_Stromverbrauch_all(kunde) {
        this.db_connection.serialize(() => {
            this.db_connection.each(`SELECT KundenID, 
                        sz.Stromverbrauch_gesamt, 
                    SUM(sz.Stromverbrauch_momentan) AS test 
                    FROM Stromzähler_Verbrauch as sz 
                    INNER JOIN Kunde_Stromzähler as k 
                    ON sz.StromzählerID=k.StromzählerID
                    WHERE KundenID = ?`,
                [kunde], (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    console.log(row);
                });
        });
    }


    close_connection() {
        this.db_connection.close((err) => {
            if (err) {
                console.error(err.message);
            }
            console.log('Close the database connection.');
        });
    }
}

module.exports = dbConnector

