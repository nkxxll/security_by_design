const sqlite3 = require('sqlite3');

class dbConnector {
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
        db.serialize(() => {
            db.each( `SELECT KundenID,
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
        db.serialize(() => {
            db.each(`SELECT KundenID, 
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
                console.log(row.id + "\t" + row.name);
            });
        });
    }


    close_connection() {
        db.close((err) => {
            if (err) {
                console.error(err.message);
            }
            console.log('Close the database connection.');
        });
    }
}

module.exports = dbConnector

