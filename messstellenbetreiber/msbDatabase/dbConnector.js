const sqlite3 = require('sqlite3');
const validator = require('validator');

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

    read_Stromverbrauch_Year(Kunden, zeitspanne_anfang, zeitspanne_ende) {
        db.serialize(() => {
            db.each(`SELECT KundenId as id,
                            Name as name
                     FROM playlists`, (err, row) => {
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