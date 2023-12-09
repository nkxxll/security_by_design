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
            this.db_connection = Null;
        }
    }
    runSQL(sql, params, response, changeOutput) {
        if (params != undefined && params != null) {
            this.db_connection.all(sql, params, (err, rows) => {
                console.log("Read:", rows);
                if (typeof changeOutput === 'function') {
                    rows = changeOutput(rows);
                }
                console.log("Sendin:", rows);
                response.send(rows);
            });
        }
    }

    /*check if key is in database*/
    test(response) {
        this.runSQL("SELECT * FROM StromzahlerVerbrauch", [], response);
    }

    /*check if key is in database*/
    exists_ZaehlerKey(zaehlerKey) {
        this.db_connection.each(`SELECT Auth_Key
                    FROM StromzahlerAuth 
                    WHERE Auth_Key = ?`,
            [zaehlerKey],
            (err, row) => {
                if (err) {
                    console.error(err.message);
                }
                console.log(row.id + "\t" + row.name);
            });
    }

    /* Stromverbrauch eines bestimmten Zeitraums */
    read_Stromverbrauch_timeframe(kunde, zeitspanne_anfang, zeitspanne_ende) {
        this.db_connection.each(`SELECT KundenID,
                        sz.StromverbrauchGesamt, 
                        SUM(sz.StromverbrauchMomentan) AS test 
                    FROM StromzahlerVerbrauch as sz 
                    INNER JOIN KundeStromzähler as k 
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
    }

    /* Stromverbrauch gesamt seid Vertragsbeginn */
    read_Stromverbrauch_all(kunde) {
        this.db_connection.serialize(() => {
            let rows = [];
            this.db_connection.each(`SELECT KundenID, 
                        sz.StromverbrauchGesamt, 
                    SUM(sz.StromverbrauchJetzt) AS test 
                    FROM StromzahlerVerbrauch as sz 
                    INNER JOIN KundeStromzähler as k 
                    ON sz.StromzählerID=k.StromzählerID
                    WHERE KundenID = ?`,
                [kunde], (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    console.log(row);
                    rows.push(row);
                });
            return rows;
        })
    }

    read_Wartungs_datum(stromzaehler_id) {
        this.db_connection.serialize(() => {
            let rows = [];
            this.db_connection.each(`INSERT INTO StromzahlerVerbrauch
                                        (StromzählerID, 
                                        StromverbrauchGesamt, 
                                        Uhrzeit)
                                    VALUES
                                        (?,
                                        ?,
                                        ?)`,
                [stromzaehler_id, timestamp, consumtion], (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    console.log(row);
                    rows.push(row);
                });
            return rows;
        })
    }

    read_Eichungs_datum() {

    }

    Dateneingabe_Stromzaehler(stromzaehler_id, timestamp, consumtion) {
        this.db_connection.serialize(() => {
            let rows = [];
            this.db_connection.each(`INSERT INTO StromzahlerVerbrauch
                                        (StromzählerID, 
                                        StromverbrauchGesamt, 
                                        Uhrzeit)
                                    VALUES
                                        (?,
                                        ?,
                                        ?)`,
                [stromzaehler_id, timestamp, consumtion], (err, row) => {
                    if (err) {
                        console.error(err.message);
                    }
                    console.log(row);
                    rows.push(row);
                });
            return rows;
        })
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

