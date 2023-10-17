const express = require('express');
const dbConnector = require("./dbConnector");
const router = express.Router();
const endpoints = "/api/v1/";
const db_type = true;
const sqlite_file = "db.sql";
const dbConnection = new dbConnector(db_type, sqlite_file);

// middleware that is specific to this router
router.use((request, response, next) => {
    console.log('Time: ', Date.now());
    authentificate(request, response);
    next();
});

function authentificate(request, response) {
    // TODO: check authnetification
    response.send("Nö du hast kein access");
    response.end();
}


router.get(endpoints + "historical_data", (request, response) => {
    response.send('Soll die Stromverbrauchsdaten eines Kunden zurückgeben');
});

router.get(endpoints + "historical_data" + "/:year", (request, response) => {
    response.send("Soll die Stromverbrauchsdaten des Jahresponse " + request.params.year + " eines Kunden zurückgeben");
});

router.get(endpoints + "historical_data" + "/:year/:month", (request, response) => {
    response.send("Soll die Stromverbrauchsdaten des Jahresponse " + request.params.year + " und Monats " + request.params.month + " eines Kunden zurückgeben");
});
module.exports = router