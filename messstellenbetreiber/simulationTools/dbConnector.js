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

